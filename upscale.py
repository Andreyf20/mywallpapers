import os
from PIL import Image

README_PATH = 'README.md'
TARGET_WIDTH = 3840
TARGET_HEIGHT = 2160

def process_images():
    with open(README_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith('| # | Name | Resolution | Preview |'):
            new_lines.append('| # | Name | Resolution | Preview | Status |\n')
        elif line.startswith('|---|------|------------|---------|'):
            new_lines.append('|---|------|------------|---------|--------|\n')
        elif line.startswith('|') and len(line.split('|')) >= 6:
            parts = [p.strip() for p in line.split('|')]
            num = parts[1]
            name = parts[2]
            res = parts[3]
            preview = parts[4]
            
            if not num.isdigit():
                new_lines.append(line)
                continue
                
            status = "Error"
            new_res = res
            
            try:
                if not os.path.exists(name):
                    status = "Error"
                else:
                    with Image.open(name) as img:
                        w, h = img.size
                        # Check if AT LEAST 4k (both dimensions >= target, OR one is strictly and scale would reduce)
                        # Actually if scale > 1, it needs upscaling to reach at least 3840x2160
                        scale = max(TARGET_WIDTH / w, TARGET_HEIGHT / h)
                        if scale <= 1.0:
                            status = "Original"
                            new_res = f"{w}×{h}"
                        else:
                            new_w = int(round(w * scale))
                            new_h = int(round(h * scale))
                            print(f"Upscaling {name} from {w}x{h} to {new_w}x{new_h}")
                            resized_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                            resized_img.save(name, quality=95)
                            status = "Resized"
                            new_res = f"{new_w}×{new_h}"
            except Exception as e:
                print(f"Error processing {name}: {e}")
                status = "Error"
            
            new_line = f"| {num} | {name} | {new_res} | {preview} | {status} |\n"
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    process_images()
