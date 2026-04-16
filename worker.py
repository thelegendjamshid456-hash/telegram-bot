import os, time, subprocess, shutil, zipfile, requests

SERVER = "PUT_YOUR_CHOREO_URL"

JOBS = "jobs"
OUT = "output"

os.makedirs(OUT, exist_ok=True)

def process(file, job_id):
    base = f"{OUT}/{job_id}"
    os.makedirs(base, exist_ok=True)

    if file.endswith(".apk"):
        subprocess.run(["jadx", file, "-d", base+"/jadx"])
        subprocess.run(["apktool", "d", file, "-o", base+"/apktool", "-f"])

        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(base+"/raw")

    if file.endswith(".so"):
            "C:/ghidra/support/analyzeHeadless.bat",
            base+"/ghidra_proj",
            "proj",
            "-import", file,
            "-deleteProject"
        ])

    shutil.make_archive(base, 'zip', base)
    return base + ".zip"


while True:
    for f in os.listdir(JOBS):
        if f.endswith(".bin"):
            job_id = f.split(".")[0]
            file_path = os.path.join(JOBS, f)

            result = process(file_path, job_id)

            print("Processed:", result)

            os.remove(file_path)

    time.sleep(10)
