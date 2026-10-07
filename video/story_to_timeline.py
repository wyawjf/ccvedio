"""Build build/timeline.json from story.json (the on-screen beats drive every shot and the score)."""
import json, sys
s = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "story.json"))
lines = [{**l, "tts": "", "sub": "", "pause": 0} for l in s["lines"]]
tl = {"duration": lines[-1]["end"], "outro": s["outro"], "silent": True, "lines": lines}
json.dump(tl, open(sys.argv[2] if len(sys.argv) > 2 else "build/timeline.json", "w"), ensure_ascii=False, indent=1)
print("duration", tl["duration"] + tl["outro"])
