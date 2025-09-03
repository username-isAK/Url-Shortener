# 🔗 URL Shortener  

A simple **Flask + MongoDB Atlas** project that lets you shorten long URLs, redirect to the original link, and automatically expire them after a fixed time (7 days).  

---

## 🚀 Features  
- Shorten any long URL into a 6-character code.  
- Redirect to original URL when visiting the short link.  
- Automatic expiry of links using MongoDB **TTL index**.  
- Simple HTML frontend (with Flask templates).  
- Stores data in **MongoDB Atlas**.  

---

## 🛠️ Tech Stack  
- **Backend**: Flask (Python)  
- **Database**: MongoDB Atlas (TTL Index for auto-expiry)  
- **Frontend**: HTML (Jinja2 templating inside Flask)  

---