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
        self.executor = ThreadPoolExecutor(max_workers=4)

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

    async def download(
        self,
        album_id: str,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Optional[Path]:
        """下载漫画

        Args:
            album_id: 漫画 ID
            progress_callback: 进度回调函数 (current, total)

        Returns:
            下载目录路径，失败返回 None
        """
        def _download():
            try:
                # 创建选项
                option = jmcomic.JmOption.default()
                option.dir_rule.base_dir = str(self.download_dir)

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
                    return downloaded_dirs[0]

                print(f"未找到下载目录")
                return None

            except Exception as e:
                print(f"下载错误: {e}")
                import traceback
                traceback.print_exc()
                return None

        # 在线程池中执行下载
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(self.executor, _download)

        # 下载完成后调用进度回调（100%）
        if result and progress_callback:
            try:
                await progress_callback(100, 100)
            except:
                pass

        return result

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
