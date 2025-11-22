# Uni Python Project — Collaboration Guide

Welcome to the team!  
This document explains **exactly how we work together in this repository**, using Git and GitHub through **PyCharm**.

---

## 🚀 1. Clone the Repository (First Step for Everyone)

1. Open **PyCharm**
2. Click **Get from VCS**
3. Paste the repository ( https://github.com/paddywestphal/intro_to_python_project.git )
4. Choose a folder → **Clone**

PyCharm will automatically set up the project and link it to Git.

---

## 🌿 2. Use Your Own Branch Only

Each user has a dedicated branch:

`patrick`
`michelle`
`fabian`
`simon`

You **must not** commit directly to `main`.

### To switch to your branch:
PyCharm → Top Left (Branch Symbol) → Remote → select **your branch**

---

## ✏️ 3. Make Changes → Commit → Push

Whenever you work on the code:

1. Modify files normally  
2. Go to **Commit** (top left branch menu or Ctrl + K)  
3. Add a clear commit message, for example:  
   - `implemented menu selection`
   - `added price lookup`
   - `fixed input validation`
4. Click **Commit & Push**

This sends your changes to **your own branch on GitHub**.

---

## 🔀 4. Creating a Pull Request (PR)

When you want your changes added to the main project:

1. Go to GitHub → **Pull Requests**
2. Click **New Pull Request**
3. **Base branch: `main`**  
   **Compare branch: your branch**
4. Write a description of what you changed
5. Submit the PR

Pull Requests ensure the main branch stays stable and nothing accidentally breaks.

---

## 👀 5. Code Review & Merge Rules

- Patrick (or assigned reviewer) checks the PR  
- If everything works → PR is **approved** and **merged**  
- If changes are needed → the reviewer will comment  

After merge: Git → Pull (in PyCharm)

This updates your local code.

---

## 🔄 6. Keep Your Branch Updated (Important)

Before you start coding each day:

1. Switch to your branch  
2. Pull the latest version of `main` into it:
via PyCharm:

**Git → Update Project** (or Strg + T)

This prevents conflicts and ensures everyone works with the latest version.

---

## 📚 7. Folder Structure (to be updated during development)

/project_root
├── src/ # program code
├── data/ # price files, etc.
├── docs/ # instructions, diagrams
├── tests/ # optional test scripts
├── README.md # this file
└── ...

---

## 🧩 8. Contribution Rules

- Always work in **your branch**  
- Keep commits small and focused  
- Commit often  
- Write meaningful commit messages  
- Don’t merge directly into `main`  
- Open a PR when you're ready  
- Coordinate major changes within the team  

---


