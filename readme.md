# 🐾 PetBook

![Django](https://img.shields.io/badge/Django-6.0.2-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Upstash-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=Cloudinary&logoColor=white)

**PetBook** is a modern, responsive, and fully-featured social network built exclusively for pets. Share moments, upload photos, and connect with other furry friends. 

🚀 **Live Demo:** [https://petbook.fly.dev](https://petbook.fly.dev)

---

## ✨ Key Features & Technical Highlights

This project was built with a strong focus on **Security (SecOps)**, **Performance**, and **Modern UX/UI**.

### 🔒 Security & Protection
* **Rate Limiting:** Implemented `django-ratelimit` to protect authentication routes against brute-force attacks and botnets (e.g., max 5 registrations/hour per IP).
* **Robust Authentication:** Custom user model supporting both Email and Username login logic.
* **SecOps on Deletions:** Database-level verification (`author=request.user`) ensures users can only modify or delete their own posts, preventing IDOR (Insecure Direct Object Reference) vulnerabilities.
* **Production-Ready Environment:** Strict enforcement of `SECURE_SSL_REDIRECT`, CSRF/Session secure cookies, and environment variables (.env) for secrets.

### ⚡ Performance & Asynchronous Tasks
* **Background Processing:** Integrated **Celery** with an **Upstash Redis** broker to handle asynchronous tasks (like sending welcome emails via SMTP) without blocking the main application thread.
* **Optimized Database Queries:** Prevented the N+1 query problem by heavily utilizing Django's `select_related` and `prefetch_related` in feed and gallery views.
* **Smart Search:** Leveraged PostgreSQL's `unaccent` extension for a seamless, diacritic-insensitive search experience (e.g., searching "Papousek" matches "Papoušek").

### 🎨 Modern Frontend & Media Handling
* **Alpine.js & TailwindCSS:** Built a highly reactive, JavaScript-light frontend featuring Dark Mode, Toast notifications (Django Messages), intersection observers for scroll animations, and interactive modals without the overhead of a large JS framework.
* **Cloudinary Integration:** Direct upload of media files to Cloudinary for automatic format optimization (WEBP) and responsive delivery. Enforced strict 20MB file limits and MIME-type validation on the backend.
* **UX Details:** Empty states for new users, custom 404 error pages, character counters, and dynamic image upload previews.

---

## 🛠️ Tech Stack Architecture

* **Framework:** Django 6.0.2
* **Database:** PostgreSQL (Hosted on Supabase)
* **Task Queue:** Celery + Redis (Hosted on Upstash)
* **Static & Media:** Cloudinary (Media files) + WhiteNoise (Static files)
* **Frontend:** TailwindCSS, Alpine.js, HTML5
* **Monitoring:** Sentry SDK for real-time error and performance tracking.
* **Deployment:** Containerized and hosted on Fly.io (Gunicorn WSGI).

---

## 🚀 CI/CD Pipeline & Deployment

The deployment process is fully automated to ensure rapid and reliable updates. 
* **GitHub Actions:** A CI/CD workflow is configured to automatically trigger upon every `git push` to the `main` branch.
* **Fly.io:** The application is containerized and continuously deployed to Fly.io.
* **Database Migrations:** Django migrations and static file collection (`collectstatic` via WhiteNoise) are handled automatically during the build phase.

This zero-downtime deployment strategy allows for seamless shipping of new features with a single git command.

---

## 🗺️ Roadmap & Future Enhancements

PetBook is continuously evolving. Here are the planned features for upcoming releases:

- [ ] **Friends & Followers System:** Establish relationships between pets (Many-to-Many database models).
- [ ] **Direct Messaging (WebSockets):** Implement Django Channels for real-time, peer-to-peer chat without page reloads.
- [ ] **Smart @Mentions:** Allow users to tag their friends in posts and comments with automatic profile linking.
- [ ] **Activity Notifications:** In-app notification hub for likes, comments, and new followers.

---
*Designed and built with ❤️ for pets and their humans.*