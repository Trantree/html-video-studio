# -*- coding: utf-8 -*-
"""Generate TTS audio and auto-calculate timeline from actual audio duration."""
import asyncio
import json
import os
import subprocess
import edge_tts

async def generate_sentence_audio(text, voice, out_path, rate="+5%"):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(out_path)

def get_audio_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    with open(args.story, "r", encoding="utf-8") as f:
        story = json.load(f)

    audio_dir = os.path.join(args.out, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    voice = story.get("voice", {}).get("name", "zh-CN-YunyangNeural")
    rate = story.get("voice", {}).get("rate", "+5%")

    timeline = []
    current_t = 0.3  # 开头留白
    for i, scene in enumerate(story["scenes"]):
        text = scene["narration"]
        audio_path = os.path.join(audio_dir, f"scene_{i:03d}.mp3")
        asyncio.run(generate_sentence_audio(text, voice, audio_path, rate))
        dur = get_audio_duration(audio_path)
        scene_start = current_t
        scene_end = current_t + dur + 0.4  # 句间换气垫
        timeline.append({"start": scene_start, "end": scene_end, "audio": audio_path})
        current_t = scene_end

    story["timeline"] = timeline
    with open(os.path.join(args.out, "story_with_timeline.json"), "w", encoding="utf-8") as f:
        json.dump(story, f, ensure_ascii=False, indent=2)
    print(f"Audio generated, total duration: {current_t:.2f}s")

if __name__ == "__main__":
    main()
