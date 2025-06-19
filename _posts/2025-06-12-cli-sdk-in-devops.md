---
layout: post
title: "Choosing Between CLI and SDK in DevOps: A Practical Guide"
date: 2025-06-12 21:46:01 +09:00
tags: []            
mermaid: true
---

> In this article, we’ll explore key considerations when choosing between CLI and SDK tools in real-world DevOps pipelines.
>
> These are the lessons and best practices I gathered from my recent MLOps production experience, highlighting how both CLI and SDK bring unique strengths to automation, deployment, and maintainability.
>
> 🙄 **tl;dr**: Use CLI for quick, one-off tasks during early development; use SDK for maintainable, semantic workflows in production — unless you're skilled at crafting reusable shell scripts, in which case you can comfortably go with either.

## Introduction

When automating tasks in a DevOps environment—especially in MLOps or cloud-native workflows—you’re often faced with a fundamental decision:

**Should you use the Command-Line Interface (CLI), the Software Development Kit (SDK)?**

> There is a third option, REST API, which is commonly used in application development for programmatic access but are less commonly invoked directly in CI/CD pipelines, since those pipelines favor scripting tools that wrap API calls for ease and reusability.

Both are viable tools for scripting, deployment, and resource management, but their trade-offs aren’t just technical—they impact developer experience, maintainability, and velocity. The CLI shines for quick, shell-native automation. The SDK, on the other hand, unlocks richer logic, modularity, and better integration into CI/CD workflows.

I’ll skip the textbook stuff. Here’s what I’ve actually learned from doing it in production.

## Host Language 

Whether you’re using a CLI or an SDK, you’re not just calling isolated commands or functions — you’re writing scripts or programs that run in a broader context. That context is what I am referring as *the host language*.

For CLI, the host language is typically a shell environment like Bash (on Linux/macOS) or PowerShell (on Windows). These are powerful, but they come with quirks, especially when handling logic, error control, or cross-platform compatibility.

For SDKs, the host language is usually a full-featured programming language like Python, JavaScript, or Java — depending on what the service provider supports (e.g., Azure ML SDK uses Python).

### Why this matters? 

The host language influences your learning curve, how readable and maintainable your scripts are, and how easily you can integrate with other systems (e.g., REST calls, file I/O, logging, etc.).

In other words, choosing between CLI and SDK isn't just about the tool itself — it's also about how comfortable and productive you (or your team) are in the host language that wraps around it.

## Runtime Setup

Getting your tools running is often the first headache—and it differs a lot between CLI and SDK.

### CLI: Simple and Lightweight

Setting up the CLI usually just means installing a tool like `az` (Azure CLI) and adding extensions like `ml`. That’s it. You don’t need to worry about Python environments, dependency conflicts, or package management. It’s quick, self-contained, and ready to go in most CI runners.

### SDK: Fragile and Heavy

The SDK route is a different story. You’ll likely be using Python (especially with Azure ML SDK), which means:

* Installing Python (and matching the expected version)
* Creating and managing a virtual environment (`.venv`)
* Installing the SDK and all its dependencies, which often pulls in a large, fragile dependency tree

Even with `requirements.txt`, things can get messy quickly. A single version mismatch or system conflict can break the whole install. SDKs are tightly coupled to runtime expectations, making CI/CD pipelines more fragile unless you pin versions and carefully manage dependencies.

### Is `.venv` still the right way to manage environments in CI/CD?

In traditional local development, Python virtual environments (`.venv`) help isolate dependencies, but in modern CI/CD pipelines, their role is less clear. Pipeline runners like GitHub Actions or Azure DevOps agents are supposed to be ephemeral — they spin up fresh environments for each job, then discard them afterward.

Running `.venv` on such one-off runners feels redundant or cumbersome because:

* The runner itself is supposed to be a clean slate each time
* Managing `.venv` adds complexity and can slow down the pipeline setup
* Dependency issues still happen if package versions aren’t strictly managed

### Containers: The modern approach to runtime isolation

Instead of relying on `.venv`, many teams now package SDK-based workflows inside Docker containers:

* Containers encapsulate the entire runtime, dependencies, and environment consistently
* They work well on CI platforms that support containerized jobs or self-hosted runners
* This “frame within a frame” approach avoids polluting the host machine and ensures reproducibility

However, running containers on top of CI runners introduces some overhead and complexity:

* You need to build and maintain container images
* Startup time can be longer compared to direct CLI or SDK installs
* Requires familiarity with container tooling and orchestration

