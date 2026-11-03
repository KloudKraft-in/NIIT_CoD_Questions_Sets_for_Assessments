import os
import socket
import boto3
import requests
from datetime import datetime
import pytz

# ---------------- Configuration ----------------
REGION = "ap-southeast-2"
CENTRAL_SERVER_TAG_KEY = "Role"
CENTRAL_SERVER_TAG_VALUE = "central-server"
VM_TAG_KEY = "LabsKraft"
# ------------------------------------------------

def get_submitter_name() -> str:
    """
    Priority:
    1. ECS explicit env var (LABSKRAFT_NAME)
    2. ECS task-id
    3. EC2 VM tag (LabsKraft)
    4. EC2 instance-id
    5. Local hostname
    """

    # ---------- 1️⃣ Explicit name (ECS Fargate best practice) ----------
    explicit_name = os.environ.get("LABSKRAFT_NAME")
    if explicit_name:
        return explicit_name

    # ---------- 2️⃣ ECS metadata fallback ----------
    ecs_meta_uri = os.environ.get("ECS_CONTAINER_METADATA_URI_V4")
    if ecs_meta_uri:
        try:
            task_meta = requests.get(f"{ecs_meta_uri}/task", timeout=2).json()
            task_arn = task_meta.get("TaskARN", "")
            task_id = task_arn.split("/")[-1] if task_arn else "unknown"
            return f"ecs_{task_id}"
        except Exception:
            return "ecs_unknown"

    # ---------- 3️⃣ EC2 / Docker-on-VM ----------
    try:
        token_resp = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            timeout=2
        )
        if token_resp.status_code != 200:
            raise Exception("IMDS token fetch failed")

        token = token_resp.text.strip()

        instance_id = requests.get(
            "http://169.254.169.254/latest/meta-data/instance-id",
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2
        ).text.strip()

        tag_url = f"http://169.254.169.254/latest/meta-data/tags/instance/{VM_TAG_KEY}"
        tag_resp = requests.get(
            tag_url,
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2
        )

        if tag_resp.status_code == 200 and tag_resp.text.strip():
            return tag_resp.text.strip()

        return f"vm_{instance_id}"

    except Exception:
        # ---------- 4️⃣ Local fallback ----------
        return f"local_{socket.gethostname()}"

def extract_problem_code(solution_path: str) -> str:
    """
    Expected path:
    <problem_code>/student_workspace/solution.py
    """
    return os.path.basename(os.path.dirname(os.path.dirname(solution_path)))

def get_central_server_public_ip() -> str | None:
    # 1️⃣ ECS / explicit env (BEST)
    env_ip = os.environ.get("CENTRAL_SERVER_IP")
    if env_ip:
        return env_ip

    # 2️⃣ EC2 fallback (VM only)
    try:
        ec2 = boto3.client("ec2", region_name=REGION)
        response = ec2.describe_instances(
            Filters=[
                {"Name": f"tag:{CENTRAL_SERVER_TAG_KEY}", "Values": [CENTRAL_SERVER_TAG_VALUE]},
                {"Name": "instance-state-name", "Values": ["running"]}
            ]
        )
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                return instance.get("PublicIpAddress")
    except Exception as e:
        print(f"[✗] Error fetching central server IP: {e}")

    return None


def submit_solution(solution_path: str):
    if not solution_path or not os.path.isfile(solution_path):
        print(f"[✗] Invalid file path: {solution_path}")
        return

    if not solution_path.endswith("solution.py"):
        print("[✗] Only solution.py files are allowed.")
        return

    submitter_name = get_submitter_name()
    problem_code = extract_problem_code(solution_path)

    public_ip = get_central_server_public_ip()
    if not public_ip:
        print("[✗] Could not retrieve central server public IP.")
        return

    url = f"http://{public_ip}:5000/submit"

    try:
        with open(solution_path, "rb") as file:
            files = {'file': file}
            data = {
                'vm_tag': submitter_name,
                'problem_code': problem_code
            }
            response = requests.post(url, files=files, data=data, timeout=60)
            response.raise_for_status()

            ist_time = datetime.now(
                pytz.timezone("Asia/Kolkata")
            ).strftime("%Y-%m-%d %H:%M:%S")

            print(f"[✓] Submission successful")
            print(f"[✓] Problem Code : {problem_code}")
            print(f"[✓] Submitted By : {submitter_name}")
            print(f"[✓] IST Time     : {ist_time}")
            print(f"[✓] Server Reply : {response.text.strip()}")

    except requests.exceptions.RequestException as e:
        print(f"[✗] Submission failed: {e}")

# ---------------- Main ----------------
if __name__ == "__main__":
    print("Enter the path to your solution.py (inside <problem_code>/student_workspace/):")
    path = input(">>> ").strip()
    if not path:
        print("[✗] No path provided.")
    else:
        submit_solution(path)
