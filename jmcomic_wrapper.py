#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JMComic API 封装
"""
import sys
from pathlib import Path
from typing import List, Dict, Optional, Callable
from PIL import Image
import asyncio
from concurrent.futures import ThreadPoolExecutor

# 添加 JMComic 库路径
jm_path = Path(__file__).parent / "JMComic-Crawler-Python" / "src"
sys.path.insert(0, str(jm_path))

import jmcomic


class JMComicAPI:
    """JMComic API 封装类"""

    def __init__(self, download_dir: Path):
        """初始化

        Args:
            download_dir: 下载目录
        """
        self.download_dir = download_dir
        self.download_dir.mkdir(exist_ok=True, parents=True)
        # 减少线程数以降低内存占用（Railway 内存限制）
        self.executor = ThreadPoolExecutor(max_workers=1)

    async def search(self, keyword: str, limit: int = 10) -> List[Dict]:
        """搜索漫画

        Args:
            keyword: 搜索关键词
            limit: 返回结果数量限制

        Returns:
            搜索结果列表，每个结果包含 id, title, author 等信息
        """
        def _search():
            try:
                # 创建选项
                option = jmcomic.JmOption.default()
                client = option.build_jm_client()

                # 搜索
                albums = client.search_site(search_query=keyword, page=1)

                if not albums or len(albums) == 0:
                    return []

                # 注意：不能用 for in 迭代 albums，因为 __iter__ 会返回简化格式
                # 必须使用索引访问才能获取完整数据
                results = []
                actual_limit = min(limit, len(albums))

                for i in range(actual_limit):
                    album = albums[i]  # 使用索引访问获取完整数据

                    if isinstance(album, tuple) and len(album) >= 2:
                        # 处理 tuple 格式: (id, data_dict)
                        album_id, album_data = album[0], album[1]
                        if isinstance(album_data, dict):
                            results.append({
                                'id': str(album_id),
                                'title': album_data.get('name', album_data.get('title', 'Unknown')),
                                'author': album_data.get('author', 'Unknown')
                            })
                        else:
                            results.append({
                                'id': str(album_id),
                                'title': str(album_data),
                                'author': 'Unknown'
                            })
                    else:
                        # 处理对象格式
                        results.append({
                            'id': str(album.id) if hasattr(album, 'id') else 'Unknown',
                            'title': album.title if hasattr(album, 'title') else 'Unknown',
                            'author': album.author if hasattr(album, 'author') else 'Unknown'
                        })

                return results

            except Exception as e:
                print(f"搜索错误: {e}")
                import traceback
                traceback.print_exc()
                return []

        # 在线程池中执行
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, _search)

    async def get_info(self, album_id: str) -> Optional[Dict]:
        """获取漫画详细信息

        Args:
            album_id: 漫画 ID

        Returns:
            漫画详细信息字典
        """
        def _get_info():
            try:
                option = jmcomic.JmOption.default()
                client = option.build_jm_client()

                # 获取专辑信息
                album = client.get_album_detail(album_id)

                # 获取页数 - 需要从 episode 获取
                page_count = 0
                if hasattr(album, 'episode_list') and album.episode_list:
                    # 获取第一个章节的详细信息
                    first_episode = album.episode_list[0]
                    if isinstance(first_episode, tuple) and len(first_episode) >= 1:
                        episode_id = first_episode[0]
                        try:
                            photo_detail = client.get_photo_detail(episode_id, fetch_album=False, fetch_scramble_id=False)
                            if hasattr(photo_detail, 'page_arr') and photo_detail.page_arr:
                                page_count = len(photo_detail.page_arr)
                        except:
                            page_count = 0

                # 处理作者信息
                author = 'Unknown'
                if hasattr(album, 'authors') and album.authors:
                    author = ', '.join(album.authors) if isinstance(album.authors, list) else str(album.authors)
                elif hasattr(album, 'author') and album.author:
                    author = ', '.join(album.author) if isinstance(album.author, list) else str(album.author)

                return {
                    'id': album_id,
                    'title': album.title if hasattr(album, 'title') else 'Unknown',
                    'author': author,
                    'tags': album.tags if hasattr(album, 'tags') else [],
                    'category': 'Unknown',
                    'page_count': page_count,
                    'update_date': album.update_date if hasattr(album, 'update_date') else 'Unknown'
                }

            except Exception as e:
                print(f"获取信息错误: {e}")
                import traceback
                traceback.print_exc()
                return None

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, _get_info)

    async def download_with_streaming(
        self,
        album_id: str,
        image_callback: Optional[Callable[[Path], None]] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Optional[Path]:
        """流式下载漫画，每下载一张就通过回调返回

        Args:
            album_id: 漫画 ID
            image_callback: 图片回调函数 (image_path)
            progress_callback: 进度回调函数 (current, total)

        Returns:
            下载目录路径，失败返回 None
        """
        download_complete = False
        result_holder = [None]
        sent_images = set()

        def _download():
            nonlocal download_complete
            try:
                # 创建选项，使用配置字典限制并发
                config = {
                    'dir_rule': {
                        'base_dir': str(self.download_dir)
                    },
                    'download': {
                        'image': {
                            'thread_count': 1  # 强制单线程
                        }
                    }
                }

                print(f"创建配置: thread_count=1")
                option = jmcomic.JmOption.construct(config, cover_default=True)
                print(f"选项已创建")

                # 下载
                print(f"开始下载漫画 {album_id}")
                jmcomic.download_album(album_id, option)
                print(f"下载完成 {album_id}")

                # 查找下载的目录
                downloaded_dirs = list(self.download_dir.glob(f"*{album_id}*"))
                if not downloaded_dirs:
                    # 查找所有新目录
                    downloaded_dirs = sorted(
                        self.download_dir.iterdir(),
                        key=lambda x: x.stat().st_mtime,
                        reverse=True
                    )

                if downloaded_dirs:
                    print(f"找到下载目录: {downloaded_dirs[0]}")
                    result_holder[0] = downloaded_dirs[0]
                else:
                    print(f"未找到下载目录")

            except Exception as e:
                print(f"下载错误: {e}")
                import traceback
                traceback.print_exc()
            finally:
                download_complete = True

        # 启动下载线程
        loop = asyncio.get_event_loop()
        download_task = loop.run_in_executor(self.executor, _download)

        # 监控下载目录，每秒检查新图片
        heartbeat_count = 0
        last_progress_update = 0

        while not download_complete:
            await asyncio.sleep(1)
            heartbeat_count += 1

            # 查找下载目录
            download_dirs = list(self.download_dir.glob(f"*{album_id}*"))
            if download_dirs:
                download_dir = download_dirs[0]

                # 查找所有图片
                image_files = sorted(download_dir.glob("*.webp"))
                if not image_files:
                    image_files = sorted(download_dir.glob("*.jpg"))
                if not image_files:
                    image_files = sorted(download_dir.glob("*.png"))

                # 发送新图片
                for img_file in image_files:
                    if img_file not in sent_images and img_file.stat().st_size > 0:
                        sent_images.add(img_file)
                        if image_callback:
                            try:
                                await image_callback(img_file)
                            except Exception as e:
                                print(f"图片回调错误: {e}")

                # 每5秒发送进度更新
                if heartbeat_count - last_progress_update >= 5:
                    last_progress_update = heartbeat_count
                    if progress_callback:
                        try:
                            await progress_callback(len(sent_images), -1)
                        except Exception as e:
                            print(f"进度回调错误: {e}")

        # 等待下载完成
        await download_task

        # 发送剩余的图片
        if result_holder[0]:
            download_dir = result_holder[0]
            image_files = sorted(download_dir.glob("*.webp"))
            if not image_files:
                image_files = sorted(download_dir.glob("*.jpg"))
            if not image_files:
                image_files = sorted(download_dir.glob("*.png"))

            for img_file in image_files:
                if img_file not in sent_images:
                    sent_images.add(img_file)
                    if image_callback:
                        try:
                            await image_callback(img_file)
                        except Exception as e:
                            print(f"图片回调错误: {e}")

        return result_holder[0]

    async def create_pdf(
        self,
        source_dir: Path,
        output_file: Path,
        quality: int = 95
    ) -> bool:
        """将图片合并为 PDF

        Args:
            source_dir: 图片源目录
            output_file: 输出 PDF 文件路径
            quality: 图片质量 (1-100)

        Returns:
            是否成功
        """
        def _create_pdf():
            images_to_close = []
            try:
                # 获取所有图片文件并排序
                image_files = sorted(source_dir.glob("*.webp"))
                if not image_files:
                    image_files = sorted(source_dir.glob("*.jpg"))
                if not image_files:
                    image_files = sorted(source_dir.glob("*.png"))

                if not image_files:
                    print("未找到图片文件")
                    return False

                print(f"找到 {len(image_files)} 个图片文件")

                # 打开第一张图片
                first_img = Image.open(image_files[0]).convert('RGB')
                images_to_close.append(first_img)
                print(f"第一张图片: {image_files[0]}, 尺寸: {first_img.size}")

                # 逐个加载剩余图片，添加到列表
                images = []
                for i, img_file in enumerate(image_files[1:], 2):
                    try:
                        img = Image.open(img_file).convert('RGB')
                        images.append(img)
                        images_to_close.append(img)

                        # 每处理5张图片打印一次进度
                        if i % 5 == 0:
                            print(f"已加载 {i}/{len(image_files)} 张图片")
                    except Exception as e:
                        print(f"加载图片失败 {img_file}: {e}")
                        continue

                print(f"成功加载所有 {len(image_files)} 张图片")

                # 保存为 PDF
                print(f"开始保存 PDF: {output_file}")
                first_img.save(
                    output_file,
                    save_all=True,
                    append_images=images,
                    resolution=100.0,
                    quality=quality,
                    optimize=False
                )

                print(f"PDF 创建成功: {output_file.stat().st_size / (1024*1024):.2f}MB")
                return True

            except MemoryError as e:
                print(f"内存不足，无法创建 PDF: {e}")
                return False
            except Exception as e:
                print(f"创建 PDF 错误: {e}")
                import traceback
                traceback.print_exc()
                return False
            finally:
                # 确保关闭所有图片
                print(f"关闭 {len(images_to_close)} 张图片")
                for img in images_to_close:
                    try:
                        img.close()
                    except:
                        pass

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, _create_pdf)

    def cleanup(self):
        """清理资源"""
        self.executor.shutdown(wait=False)
