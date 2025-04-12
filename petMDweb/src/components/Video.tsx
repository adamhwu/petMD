---
const { websocketUrl = "ws://<raspberry_pi_ip>:8765" } = Astro.props;
---

<style>
  .card {
    background: white;
    border-radius: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 1rem;
  }
  .video-container {
    background: black;
    border-radius: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 1rem;
  }
  video {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
  }
</style>

<!--Video Feed Card-- >
<div class="card">
  <h2>Live Video Feed</h2>
  <div class="video-container">

  </div>
</div>

<script is:client>
  const socket = new WebSocket(import.meta.env.PUBLIC_SOCKET_URL || "{websocketUrl}");

  socket.addEventListener("message", (event) => {
    const img = document.getElementById("video-stream");
    img.src = "data:image/jpeg;base64," + event.data;
  });
</script>
