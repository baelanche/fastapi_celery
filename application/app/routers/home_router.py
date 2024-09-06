from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get('/', response_class=HTMLResponse)
async def home():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>FastAPI with Celery</title>
        </head>
        <body>
            <h1>Submit a Task</h1>
            <button onclick="startDelayTask()">Start Delay 10 seconds Task</button>
            <p id="status1"></p>

            <br/><br/>
            <button onclick="startDelayCacheTask()">Start Delay Task with Caching</button>
            <p id="status2"></p>

            <script>
            async function startDelayTask() {
                document.getElementById("status1").innerText = "Task is being processed...";

                let response = await fetch(`/api/celery/delay`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                let data = await response.json();
                let pollInterval = setInterval(async () => {
                    let statusResponse = await fetch(`/api/celery/delay?task_id=${data.task_id}`);
                    let statusData = await statusResponse.json();

                    if (statusData.status === "Task completed") {
                        document.getElementById("status1").innerText = statusData.result;
                        clearInterval(pollInterval);
                    } else if (statusData.status === "Task failed") {
                        document.getElementById("status1").innerText = statusData.result;
                        clearInterval(pollInterval);
                    } else {
                        document.getElementById("status1").innerText = statusData.status;
                    }
                }, 2000);
            }

            async function startDelayCacheTask() {
                document.getElementById("status2").innerText = "Task is being processed...";

                const jsonData = {
                    id: 'abcde'
                }
                
                let response = await fetch(`/api/celery/delay/cache`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(jsonData)
                });

                let data = await response.json();

                if (data.result !== undefined) {
                    document.getElementById("status2").innerText = data.result;
                    return;
                }

                let pollInterval = setInterval(async () => {
                    let statusResponse = await fetch(`/api/celery/delay/cache?id=${jsonData.id}&task_id=${data.task_id}`);
                    let statusData = await statusResponse.json();

                    if (statusData.status === "Task completed") {
                        document.getElementById("status2").innerText = statusData.result;
                        clearInterval(pollInterval);
                    } else if (statusData.status === "Task failed") {
                        document.getElementById("status2").innerText = statusData.result;
                        clearInterval(pollInterval);
                    } else {
                        document.getElementById("status2").innerText = statusData.status;
                    }
                }, 2000);
            }
            </script>
        </body>
        </html>
        """