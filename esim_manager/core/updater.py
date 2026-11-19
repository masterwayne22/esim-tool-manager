import requests
from esim_manager.config import TOOLS_CONFIG
from esim_manager.utils.logger import logger

class UpdateManager:
    @staticmethod
    def check_upstream_version(tool_id: str) -> dict:
        info = TOOLS_CONFIG.get(tool_id)
        if not info or "upstream_api" not in info:
            return {"supported": False, "latest": "Unknown"}

        api_url = info["upstream_api"]
        try:
            headers = {"User-Agent": "eSim-Tool-Manager"}
            response = requests.get(api_url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # For GitHub API
                if "tag_name" in data:
                    latest = data["tag_name"].lstrip("v")
                    return {"supported": True, "latest": latest}
                # For SourceForge API
                elif "platform_releases" in data:
                    filename = data.get("release", {}).get("filename", "")
                    return {"supported": True, "latest": filename.split("/")[-1]}
        except Exception as e:
            logger.warning(f"Could not fetch upstream version for {tool_id}: {e}")

        return {"supported": False, "latest": "Offline/Unavailable"}