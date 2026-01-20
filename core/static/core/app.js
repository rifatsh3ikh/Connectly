function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// LIKE HANDLER
document.querySelectorAll(".like-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const postId = btn.dataset.post;

        fetch(`/like/${postId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            }
        })
        .then(res => res.json())
        .then(data => {
            btn.innerText = `❤️ ${data.likes_count}`;
        });
    });
});

// COMMENT HANDLER
document.querySelectorAll(".comment-form").forEach(form => {
    form.addEventListener("submit", e => {
        e.preventDefault();

        const postId = form.dataset.post;
        const input = form.querySelector("input");

        fetch(`/comment/${postId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `comment=${input.value}`
        })
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById(`comments-${postId}`);
            list.innerHTML += `<p><strong>${data.username}</strong>: ${data.text}</p>`;
            input.value = "";
        });
    });
});

let page = 1;
let loading = false;

window.addEventListener("scroll", () => {
    if (loading) return;

    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 50) {
        loading = true;
        page++;

        fetch(`/load-posts/?page=${page}`)
            .then(res => res.json())
            .then(posts => {
                posts.forEach(p => {
                    const div = document.createElement("div");
                    div.innerHTML = `<p><strong>${p.author}</strong>: ${p.content}</p><hr>`;
                    document.getElementById("feed").appendChild(div);
                });
                loading = false;
            });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("darkModeBtn");

    if (!btn) return;

    btn.addEventListener("click", function () {
        document.body.classList.toggle("dark");
    });
});

const darkModeBtn = document.getElementById("darkModeBtn");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

  // 1️⃣ Apply theme on page load
  function applyTheme(theme) {
    if (theme === "dark") {
      document.body.classList.add("dark");
      if (darkModeBtn) darkModeBtn.textContent = "☀️";
    } else {
      document.body.classList.remove("dark");
      if (darkModeBtn) darkModeBtn.textContent = "🌙";
    }
  }

  // 2️⃣ Determine initial theme
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme) {
    applyTheme(savedTheme); // user choice wins
  } else {
    applyTheme(prefersDark.matches ? "dark" : "light"); // system preference
  }

  // 3️⃣ Toggle manually
  darkModeBtn?.addEventListener("click", () => {
    const isDark = document.body.classList.toggle("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");
    applyTheme(isDark ? "dark" : "light");
  });

  // 4️⃣ Auto-update if system theme changes (optional but PRO)
  prefersDark.addEventListener("change", (e) => {
    if (!localStorage.getItem("theme")) {
      applyTheme(e.matches ? "dark" : "light");
    }
  });
  if (localStorage.getItem("theme") === "dark") {
    document.documentElement.classList.add("dark");
  }

  function togglePassword(inputId, icon) {
    const input = document.getElementById(inputId);
  
    if (!input) {
      console.error("Password input not found:", inputId);
      return;
    }
  
    if (input.type === "password") {
      input.type = "text";
      icon.textContent = "🙈";
    } else {
      input.type = "password";
      icon.textContent = "👁";
    }
  }