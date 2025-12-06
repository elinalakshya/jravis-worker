import os
import subprocess

# Search for worker.py everywhere
print("🔍 Searching for worker.py ...")

target = None
for root, dirs, files in os.walk("."):
    if "worker.py" in files and "memory" not in root and "publishing" not in root:
        target = os.path.join(root, "worker.py")
        break

if not target:
    print("❌ ERROR: Could not find worker.py")
    exit(1)

print(f"✅ Found worker at: {target}")
print("🚀 Launching JRAVIS Worker...\n")

subprocess.run(["python", target, "--force"])
