import docker
import os
import tarfile
import io

def create_tar_archive(files_dict):
    """
    Helper: Converts a dictionary of {filename: content} into a TAR archive 
    stream, which is required to copy files into a Docker container.
    """
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w') as tar:
        for filename, content in files_dict.items():
            encoded = content.encode('utf-8')
            info = tarfile.TarInfo(name=filename)
            info.size = len(encoded)
            tar.addfile(info, io.BytesIO(encoded))
    stream.seek(0)
    return stream

def run_tests(test_code: str, solution_code: str) -> dict:
    client = docker.from_env()
    
    # 1. Prepare the container
    try:
        # We build the image once (or use existing). 
        # Using the Dockerfile in the current directory.
        image, _ = client.images.build(path=".", tag="code-twin-sandbox")
        
        # 2. Start the container in the background
        # 'detach=True' keeps it running so we can copy files in
        # 'tty=True' keeps it alive
        container = client.containers.run(
            "code-twin-sandbox", 
            detach=True, 
            tty=True,
            # vital for security: disconnect from network if you want strict sandboxing
            network_disabled=True 
        )
        
        try:
            # 3. Copy files into the container
            files = {
                "solution.py": solution_code,
                "test_generated.py": test_code
            }
            tar_stream = create_tar_archive(files)
            container.put_archive("/app", tar_stream)
            
            # 4. Run pytest inside the container
            # This executes the command inside the isolated Linux environment
            exec_result = container.exec_run("pytest test_generated.py", workdir="/app")
            
            output = exec_result.output.decode("utf-8")
            exit_code = exec_result.exit_code
            
            return {
                "success": exit_code == 0,
                "output": output
            }
            
        finally:
            # 5. Cleanup: Always kill and remove the container
            container.stop()
            container.remove()

    except docker.errors.DockerException as e:
        return {
            "success": False,
            "output": f"Docker Error: {str(e)}\nIs Docker Desktop running?"
        }
    except Exception as e:
        return {
            "success": False,
            "output": f"System Error: {str(e)}"
        }