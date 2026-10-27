# -*- coding: utf-8 -*-
"""Render story to video using Playwright screenshots and ffmpeg."""
import json
import os
import subprocess
from playwright.sync_api import sync_playwright

def render_frames(story_path, out_dir, fps=30):
    with open(story_path, "r", encoding="utf-8") as f:
        story = json.load(f)
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(f"file://{os.path.abspath('templates/base.html')}")

        for i, (scene, t) in enumerate(zip(story["scenes"], story["timeline"])):
            duration = t["end"] - t["start"]
            frame_count = int(duration * fps)
            # Inject scene data into page
            page.evaluate(f"window.renderScene({json.dumps(scene)});")
            for frame in range(frame_count):
                page.screenshot(path=os.path.join(frames_dir, f"frame_{i:04d}_{frame:04d}.png"))
        browser.close()

    # Combine frames to video
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        os.path.join(out_dir, "video.mp4")
    ])
    # Mux with audio
    subprocess.run([
        "ffmpeg", "-y", "-i", os.path.join(out_dir, "video.mp4"),
        "-i", os.path.join(out_dir, "audio.m4a"),
        "-c:v", "copy", "-c:a", "aac",
        os.path.join(out_dir, "final.mp4")
    ])
    print("Video rendered to final.mp4")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--mode", default="full")
    args = parser.parse_args()
    story_path = os.path.join(args.out, "story_with_timeline.json")
    render_frames(story_path, args.out)
