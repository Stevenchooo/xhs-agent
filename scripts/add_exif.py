#!/usr/bin/env python3
"""
EXIF 信息添加工具
为AI生成的图片添加逼真的相机EXIF信息，并清除所有来源、创作者等元数据字段。
处理指定文件夹中的所有图片，直接替换原始文件，不改变图片内容。

用法: python add_exif.py <图片文件夹路径>
示例: python add_exif.py ./xhs_agent/data

依赖: pip install Pillow piexif
"""

import os
import sys
import math
import struct
import random
import argparse
import subprocess
import platform
from datetime import datetime, timedelta

try:
    from PIL import Image
    import piexif
except ImportError:
    print("请先安装依赖库:")
    print("  pip install Pillow piexif")
    sys.exit(1)


# ============================================================
# 相机配置文件 — 模拟真实相机拍摄参数
# ============================================================
CAMERA_PROFILES = [
    {
        "make": "SONY",
        "model": "ILCE-9M3",
        "software": "ILCE-9M3 v3.01",
        "lens_make": "SONY",
        "lens_model": "FE 70-200mm F2.8 GM OSS II",
        "focal_lengths": [70, 85, 100, 135, 200],
        "apertures": [2.8, 4.0, 5.6, 8.0],
        "max_aperture": 2.8,
        "iso_range": [100, 200, 400, 800, 1600, 3200, 6400],
        "crop_factor": 1.0,
    },
    {
        "make": "SONY",
        "model": "ILCE-9M3",
        "software": "ILCE-9M3 v3.01",
        "lens_make": "SONY",
        "lens_model": "FE 24-70mm F2.8 GM II",
        "focal_lengths": [24, 28, 35, 50, 70],
        "apertures": [2.8, 4.0, 5.6, 8.0],
        "max_aperture": 2.8,
        "iso_range": [100, 200, 400, 800, 1600, 3200, 6400],
        "crop_factor": 1.0,
    },
    {
        "make": "SONY",
        "model": "ILCE-9M3",
        "software": "ILCE-9M3 v3.01",
        "lens_make": "SONY",
        "lens_model": "FE 50mm F1.2 GM",
        "focal_lengths": [50],
        "apertures": [1.2, 1.4, 2.0, 2.8, 4.0, 5.6],
        "max_aperture": 1.2,
        "iso_range": [100, 200, 400, 800, 1600, 3200],
        "crop_factor": 1.0,
    },
    {
        "make": "Apple",
        "model": "iPhone 17 Pro Max",
        "software": "19.0.1",
        "lens_make": "Apple",
        "lens_model": "iPhone 17 Pro Max back triple camera 6.86mm f/1.6",
        "focal_lengths": [6.86],
        "apertures": [1.6],
        "max_aperture": 1.6,
        "iso_range": [50, 64, 100, 200, 400, 800],
        "crop_factor": 5.6,
    },
]


# ============================================================
# 工具函数
# ============================================================

def rational(numerator, denominator=1):
    """创建 EXIF 有理数元组 (分子, 分母)"""
    return (int(numerator), int(denominator))


def float_to_rational(value, precision=1000):
    """将浮点数转换为有理数元组"""
    return (int(round(value * precision)), precision)


def generate_random_datetime(days_back=365):
    """生成一个随机的拍摄日期时间（近 N 天内，偏向白天时段）"""
    now = datetime.now()
    delta = timedelta(
        days=random.randint(1, days_back),
        hours=random.randint(7, 20),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    dt = now - delta
    return dt.strftime("%Y:%m:%d %H:%M:%S")


# ============================================================
# EXIF 数据生成
# ============================================================

def generate_exif_dict(width, height, fixed_profile=None):
    """
    生成一套逼真的 EXIF 数据字典。

    Args:
        width:  图片宽度（像素）
        height: 图片高度（像素）
        fixed_profile: 指定使用的相机配置（为 None 时随机选取）

    Returns:
        (exif_dict, camera_model): piexif 格式的 EXIF 字典 + 相机型号名称
    """
    profile = fixed_profile if fixed_profile else random.choice(CAMERA_PROFILES)

    # --- 拍摄参数 ---
    focal_length = random.choice(profile["focal_lengths"])
    aperture = random.choice(profile["apertures"])
    iso = random.choice(profile["iso_range"])

    # 根据场景亮度计算曝光时间
    # EV100 = log2(N^2 / t)  =>  t = N^2 / 2^EV100
    # 然后用 ISO 补偿: t_real = t * 100 / ISO
    target_ev = random.uniform(9, 15)  # 从阴天室内(9)到晴天户外(15)
    exposure_time = (aperture ** 2) * 100.0 / (iso * (2 ** target_ev))

    # 吻合到常见快门速度
    common_denominators = [8000, 6400, 5000, 4000, 3200, 2500, 2000,
                           1600, 1250, 1000, 800, 640, 500, 400,
                           320, 250, 200, 160, 125, 100, 80, 60,
                           50, 40, 30, 25, 20, 15, 13, 10, 8, 6, 5, 4]
    best_denom = min(common_denominators,
                     key=lambda d: abs(1.0 / d - exposure_time))
    exposure_num = 1
    exposure_den = best_denom

    # --- 日期时间 ---
    date_time = generate_random_datetime()

    # --- APEX 值 ---
    aperture_value = 2 * math.log2(aperture)
    actual_exposure = exposure_num / exposure_den
    shutter_speed_value = -math.log2(actual_exposure) if actual_exposure > 0 else 10.0
    max_aperture_value = 2 * math.log2(profile["max_aperture"])

    # 35mm 等效焦距
    focal_length_35mm = int(round(focal_length * profile["crop_factor"]))

    # 曝光补偿（多数为 0，偶尔微调）
    bias_choices = [(0, 1), (1, 3), (-1, 3), (2, 3), (-2, 3)]
    bias_weights = [0.6, 0.1, 0.1, 0.1, 0.1]
    exposure_bias = random.choices(bias_choices, weights=bias_weights, k=1)[0]

    # --- 构建 EXIF 字典 ---
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: profile["make"].encode("utf-8"),
            piexif.ImageIFD.Model: profile["model"].encode("utf-8"),
            piexif.ImageIFD.Software: profile["software"].encode("utf-8"),
            piexif.ImageIFD.DateTime: date_time.encode("utf-8"),
            piexif.ImageIFD.Orientation: 1,
            piexif.ImageIFD.XResolution: rational(72),
            piexif.ImageIFD.YResolution: rational(72),
            piexif.ImageIFD.ResolutionUnit: 2,
            piexif.ImageIFD.YCbCrPositioning: 1,
        },
        "Exif": {
            piexif.ExifIFD.ExposureTime: rational(exposure_num, exposure_den),
            piexif.ExifIFD.FNumber: float_to_rational(aperture, 10),
            piexif.ExifIFD.ExposureProgram: random.choice([2, 3, 4]),
            piexif.ExifIFD.ISOSpeedRatings: iso,
            piexif.ExifIFD.ExifVersion: b"0232",
            piexif.ExifIFD.DateTimeOriginal: date_time.encode("utf-8"),
            piexif.ExifIFD.DateTimeDigitized: date_time.encode("utf-8"),
            piexif.ExifIFD.ComponentsConfiguration: b"\x01\x02\x03\x00",
            piexif.ExifIFD.ShutterSpeedValue: float_to_rational(shutter_speed_value),
            piexif.ExifIFD.ApertureValue: float_to_rational(aperture_value),
            piexif.ExifIFD.ExposureBiasValue: exposure_bias,
            piexif.ExifIFD.MaxApertureValue: float_to_rational(max_aperture_value),
            piexif.ExifIFD.MeteringMode: random.choice([2, 5]),
            piexif.ExifIFD.Flash: 0,
            piexif.ExifIFD.FocalLength: rational(focal_length * 100, 100),
            piexif.ExifIFD.ColorSpace: 1,
            piexif.ExifIFD.PixelXDimension: width,
            piexif.ExifIFD.PixelYDimension: height,
            piexif.ExifIFD.FlashpixVersion: b"0100",
            piexif.ExifIFD.FocalLengthIn35mmFilm: focal_length_35mm,
            piexif.ExifIFD.SceneCaptureType: random.choice([0, 1, 2]),
            piexif.ExifIFD.WhiteBalance: 0,
            piexif.ExifIFD.ExposureMode: 0,
            piexif.ExifIFD.SensingMethod: 2,
            piexif.ExifIFD.LensMake: profile["lens_make"].encode("utf-8"),
            piexif.ExifIFD.LensModel: profile["lens_model"].encode("utf-8"),
        },
        "GPS": {},
        "1st": {},
    }

    return exif_dict, profile["model"]


# ============================================================
# JPEG 无损元数据清除
# ============================================================

def strip_jpeg_metadata(jpeg_data):
    """
    从 JPEG 字节数据中无损移除所有元数据段。
    保留 APP0 (JFIF) 和全部图像数据段，不接触压缩像素数据。

    清除的内容:
      APP1  — EXIF / XMP
      APP2  — ICC Profile（重建后由显示设备按 sRGB 处理）
      APP3-APP15 — 其他元数据
      COM   — 注释
    """
    if jpeg_data[:2] != b"\xff\xd8":
        raise ValueError("不是有效的 JPEG 文件")

    output = bytearray(b"\xff\xd8")
    pos = 2

    while pos < len(jpeg_data) - 1:
        if jpeg_data[pos] != 0xFF:
            # 非标记字节 → 已进入原始数据区域，保留剩余内容
            output.extend(jpeg_data[pos:])
            break

        marker = jpeg_data[pos + 1]

        # 填充字节 0xFF
        if marker == 0xFF:
            pos += 1
            continue

        # SOI (已在开头写入)
        if marker == 0xD8:
            pos += 2
            continue

        # EOI
        if marker == 0xD9:
            output.extend(b"\xff\xd9")
            break

        # RST0-RST7（无长度字段）
        if 0xD0 <= marker <= 0xD7:
            output.extend(jpeg_data[pos:pos + 2])
            pos += 2
            continue

        # SOS — 扫描数据起始，后续为压缩图像数据，全部保留
        if marker == 0xDA:
            output.extend(jpeg_data[pos:])
            break

        # ---- 有长度字段的标记 ----
        if pos + 4 > len(jpeg_data):
            output.extend(jpeg_data[pos:])
            break

        seg_length = struct.unpack(">H", jpeg_data[pos + 2:pos + 4])[0]
        segment = jpeg_data[pos:pos + 2 + seg_length]

        if marker == 0xE0:  # APP0 (JFIF) — 保留
            output.extend(segment)
        elif 0xE1 <= marker <= 0xEF:  # APP1-APP15（元数据）— 移除
            pass
        elif marker == 0xFE:  # COM（注释）— 移除
            pass
        else:
            # DQT / DHT / SOF / DRI 等图像必需段 — 保留
            output.extend(segment)

        pos += 2 + seg_length

    return bytes(output)


# ============================================================
# macOS 扩展属性清除（来源、隔离标记等）
# ============================================================

# 需要清除的 macOS 扩展属性（包含下载来源、隔离标记等）
XATTR_TO_REMOVE = [
    "com.apple.metadata:kMDItemWhereFroms",   # 下载来源 URL
    "com.apple.metadata:kMDItemDownloadedDate",  # 下载日期
    "com.apple.quarantine",                    # 隔离/安全标记
    "com.apple.provenance",                    # 来源追踪
    "com.apple.lastuseddate#PS",               # 最近使用日期
    "com.apple.macl",                          # 访问控制
    "com.apple.metadata:_kMDItemUserTags",     # 用户标签
    "com.apple.FinderInfo",                    # Finder 信息
]


def strip_macos_xattr(filepath):
    """清除文件上的 macOS 扩展属性（来源、隔离标记等）"""
    if platform.system() != "Darwin":
        return

    for attr in XATTR_TO_REMOVE:
        try:
            subprocess.run(
                ["xattr", "-d", attr, filepath],
                capture_output=True,
            )
        except Exception:
            pass


# ============================================================
# 各格式处理函数
# ============================================================

def process_jpeg(filepath, fixed_profile=None):
    """处理 JPEG: 无损清除全部元数据 → 写入新 EXIF"""
    with Image.open(filepath) as img:
        width, height = img.size

    with open(filepath, "rb") as f:
        raw_data = f.read()

    # 1. 无损清除所有元数据段
    clean_data = strip_jpeg_metadata(raw_data)

    # 2. 生成逼真 EXIF
    exif_dict, camera_model = generate_exif_dict(width, height, fixed_profile)
    exif_bytes = piexif.dump(exif_dict)

    # 3. 无损插入新 EXIF（仅操作 APP1 段，不动压缩数据）
    final_data = piexif.insert(exif_bytes, clean_data)

    with open(filepath, "wb") as f:
        f.write(final_data)

    # 清除 macOS 扩展属性（来源等）
    strip_macos_xattr(filepath)

    return camera_model


def process_png(filepath, fixed_profile=None):
    """处理 PNG: 清除元数据 → 写入新 EXIF（PNG 为无损格式，像素不变）"""
    with Image.open(filepath) as img:
        width, height = img.size
        pixel_data = img.copy()

    # 清空所有附加信息（tEXt / iTXt / zTXt 等 AI 工具水印）
    pixel_data.info = {}

    # 生成逼真 EXIF
    exif_dict, camera_model = generate_exif_dict(width, height, fixed_profile)
    exif_bytes = piexif.dump(exif_dict)

    # 保存（PNG 无损，像素内容不变）
    pixel_data.save(filepath, format="PNG", exif=exif_bytes)

    # 清除 macOS 扩展属性（来源等）
    strip_macos_xattr(filepath)

    return camera_model


def process_webp(filepath, fixed_profile=None):
    """处理 WebP: 清除元数据 → 写入新 EXIF（quality=100 近无损保存）"""
    with Image.open(filepath) as img:
        width, height = img.size
        pixel_data = img.copy()

    pixel_data.info = {}

    exif_dict, camera_model = generate_exif_dict(width, height, fixed_profile)
    exif_bytes = piexif.dump(exif_dict)

    # WebP quality=100 尽可能减少重压缩损失
    pixel_data.save(filepath, format="WEBP", exif=exif_bytes, quality=100, method=6)

    # 清除 macOS 扩展属性（来源等）
    strip_macos_xattr(filepath)

    return camera_model


# ============================================================
# 主程序
# ============================================================

SUPPORTED_FORMATS = {
    ".jpg":  process_jpeg,
    ".jpeg": process_jpeg,
    ".png":  process_png,
    ".webp": process_webp,
}


def find_camera_profile(keyword):
    """
    根据关键词匹配相机配置（不区分大小写）。
    匹配 make 或 model 字段，返回所有匹配的配置列表。
    """
    keyword_lower = keyword.lower()
    matches = [p for p in CAMERA_PROFILES
               if keyword_lower in p["make"].lower()
               or keyword_lower in p["model"].lower()]
    return matches


def list_cameras():
    """打印所有可用的相机配置"""
    print("可用相机列表:")
    print("-" * 60)
    for i, p in enumerate(CAMERA_PROFILES):
        print(f"  [{i}]  {p['model']}  ({p['make']})")
        print(f"       镜头: {p['lens_model']}")
    print("-" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="EXIF 信息添加工具 — 为图片添加逼真的相机 EXIF 并清除来源/创作者元数据",
    )
    parser.add_argument("folder", nargs="?", help="图片文件夹路径")
    parser.add_argument(
        "--camera", "-c", type=str, default=None,
        help="指定相机（品牌/型号关键词，如 sony、ILCE-1；或序号如 0）。所有图片将统一使用该相机。",
    )
    parser.add_argument(
        "--list-cameras", "-l", action="store_true",
        help="列出所有可用的相机配置",
    )

    args = parser.parse_args()

    # 列出相机
    if args.list_cameras:
        list_cameras()
        sys.exit(0)

    if not args.folder:
        parser.print_help()
        print()
        print(f"支持格式: {', '.join(SUPPORTED_FORMATS.keys())}")
        print()
        print("示例:")
        print("  python add_exif.py ./data                     # 随机相机")
        print("  python add_exif.py ./data --camera sony        # 统一使用索尼")
        print("  python add_exif.py ./data --camera 0           # 使用列表中序号 0 的相机")
        print("  python add_exif.py --list-cameras              # 查看可用相机")
        sys.exit(1)

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"错误: '{folder}' 不是有效的文件夹路径")
        sys.exit(1)

    # 解析 --camera 参数
    fixed_profile = None
    camera_label = "随机"
    if args.camera:
        # 尝试按序号匹配
        try:
            idx = int(args.camera)
            if 0 <= idx < len(CAMERA_PROFILES):
                fixed_profile = CAMERA_PROFILES[idx]
            else:
                print(f"错误: 相机序号 {idx} 超出范围 (0-{len(CAMERA_PROFILES)-1})")
                sys.exit(1)
        except ValueError:
            # 按关键词匹配
            matches = find_camera_profile(args.camera)
            if not matches:
                print(f"错误: 未找到匹配 '{args.camera}' 的相机")
                print("提示: 使用 --list-cameras 查看可用相机")
                sys.exit(1)
            # 取第一个匹配（列表中最新的排在前面）
            fixed_profile = matches[0]

        camera_label = f"{fixed_profile['model']} ({fixed_profile['make']})"

    # 收集待处理图片
    image_files = []
    for filename in sorted(os.listdir(folder)):
        ext = os.path.splitext(filename)[1].lower()
        if ext in SUPPORTED_FORMATS:
            image_files.append((filename, ext))

    if not image_files:
        print(f"在 '{folder}' 中未找到支持的图片文件")
        print(f"支持的格式: {', '.join(SUPPORTED_FORMATS.keys())}")
        sys.exit(0)

    print(f"EXIF 信息添加工具")
    print(f"{'=' * 60}")
    print(f"目标文件夹: {os.path.abspath(folder)}")
    print(f"指定相机:   {camera_label}")
    print(f"找到 {len(image_files)} 个图片文件")
    print(f"{'=' * 60}")

    success_count = 0
    fail_count = 0

    for filename, ext in image_files:
        filepath = os.path.join(folder, filename)
        processor = SUPPORTED_FORMATS[ext]

        try:
            camera_model = processor(filepath, fixed_profile)
            print(f"  ✓ {filename}  →  {camera_model}")
            success_count += 1
        except Exception as e:
            print(f"  ✗ {filename}  →  错误: {e}")
            fail_count += 1

    print(f"{'=' * 60}")
    print(f"处理完成:  成功 {success_count}  |  失败 {fail_count}")


if __name__ == "__main__":
    main()
