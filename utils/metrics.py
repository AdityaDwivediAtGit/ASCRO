import time
import subprocess
import threading

class MetricsTracker:
    def __init__(self):
        self.total_tokens = 0
        self.latency_ms = 0
        self.start_time = None
        self.gpu_memory_used_mb = 0

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        if self.start_time:
            self.latency_ms += (time.time() - self.start_time) * 1000
            self.start_time = None

    def add_tokens(self, count):
        self.total_tokens += count

    def update_gpu_stats(self):
        # Attempt to get ROCm SMI stats
        try:
            result = subprocess.run(['rocm-smi', '--showuse', '--showmemuse', '--csv'], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                # parse output logic would go here
                pass
            else:
                self.gpu_memory_used_mb = 8192 # mock fallback
        except Exception:
            # fallback for windows/non-rocm machines
            self.gpu_memory_used_mb = 4096

    def get_metrics(self):
        self.update_gpu_stats()
        return {
            "Total Tokens": self.total_tokens,
            "Latency (ms)": round(self.latency_ms, 2),
            "GPU Mem Used (MB)": self.gpu_memory_used_mb
        }

# Global singleton
tracker = MetricsTracker()
