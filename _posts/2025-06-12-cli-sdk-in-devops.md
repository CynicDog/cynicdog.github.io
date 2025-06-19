---
layout: post
title: "Learning CLI and SDK in DevOps: Reflections from Real Work"
date: 2025-06-12 21:46:01 +09:00
tags: []            
mermaid: true
---

> In this article, we’ll explore key considerations when choosing between CLI and SDK tools in real-world DevOps pipelines.
>
> These are the lessons and best practices I gathered from my recent MLOps production experience, highlighting how both CLI and SDK bring unique strengths to automation, deployment, and maintainability.
>
> 🙄 **tl;dr**: Use CLI for quick, one-off tasks during early development; use SDK for maintainable, semantic workflows in production — unless you're skilled at crafting reusable shell scripts, in which case you can comfortably go with either.

## 0. Introduction

When automating tasks in a DevOps environment—especially in MLOps or cloud-native workflows—you’re often faced with a fundamental decision:

**Should you use the Command-Line Interface (CLI), the Software Development Kit (SDK)?**

> There is a third option, REST API, which is commonly used in application development for programmatic access but are less commonly invoked directly in CI/CD pipelines, since those pipelines favor scripting tools that wrap API calls for ease and reusability.

Both are viable tools for scripting, deployment, and resource management, but their trade-offs aren’t just technical—they impact developer experience, maintainability, and velocity. The CLI shines for quick, shell-native automation. The SDK, on the other hand, unlocks richer logic, modularity, and better integration into CI/CD workflows.

I’ll skip the textbook stuff. Here’s what I’ve actually learned from doing it in production.

## 1. Host Language 

Whether you’re using a CLI or an SDK, you’re not just calling isolated commands or functions — you’re writing scripts or programs that run in a broader context. That context is what I am referring as *the host language*.

For CLI, the host language is typically a shell environment like Bash (on Linux/macOS) or PowerShell (on Windows). These are powerful, but they come with quirks, especially when handling logic, error control, or cross-platform compatibility.

For SDKs, the host language is usually a full-featured programming language like Python, JavaScript, or Java — depending on what the service provider supports (e.g., Azure ML SDK uses Python).

### Why this matters? 

The host language influences your learning curve, how readable and maintainable your scripts are, and how easily you can integrate with other systems (e.g., REST calls, file I/O, logging, etc.).

In other words, choosing between CLI and SDK isn't just about the tool itself — it's also about how comfortable and productive you (or your team) are in the host language that wraps around it.

## 2. Runtime Setup

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

In traditional local development, Python virtual environments (`.venv`) are a handy way to isolate dependencies and avoid conflicts. However, in modern CI/CD pipelines, their role is less clear. Platforms like GitHub Actions or Azure DevOps spin up fresh runner environments for each job and discard them once the job completes. Because of this ephemeral nature, managing a `.venv` inside the pipeline can feel redundant and add unnecessary complexity.

Since each runner starts as a clean slate, setting up a virtual environment within it might slow down the pipeline without delivering significant benefits. Additionally, dependency issues can still arise if package versions aren’t strictly controlled, so `.venv` alone doesn’t guarantee stability.

### Containers: The modern approach to runtime isolation

To address these challenges, many teams are moving toward packaging SDK-based workflows inside Docker containers. Containers encapsulate the entire runtime, dependencies, and environment in a single, consistent image. This approach works well on CI platforms that support containerized jobs or self-hosted runners and helps avoid polluting the host machine.

Using containers in CI is like running “a frame within a frame” — your workflow runs inside a container, which itself runs on the ephemeral CI runner. This ensures reproducibility and isolates your environment from host inconsistencies.

That said, running containers introduces some overhead. Building and maintaining container images requires additional effort, and container startup times are often longer than directly installing CLI tools or SDKs on the runner. It also requires some familiarity with container tooling and orchestration, which might add to the learning curve.

## 3. Modularity and Reusability

One of the biggest limitations of using CLI is that its output is fundamentally just plain text. Whether it’s JSON, table format, or even written to a file, you still end up with raw strings to work with. For example, if you run a command like `az ml job show` to check a job’s status, you have to parse the JSON output manually, extract specific keys, and write conditional logic around string values like `status="Running"`. Even if you use parsing tools like `jq`, the process remains quite manual and brittle. This quickly becomes dry and hardcoded, lacking semantic meaning.

Error handling with CLI is also challenging because many errors are sent as unstructured text to standard error (stderr). This forces you to rely on fragile string matching and guesswork to detect failure conditions.

In contrast, SDKs provide a much richer and structured programming experience:

* SDK responses are object instances with clear attributes and methods, allowing you to work with meaningful data rather than raw text.
* You can easily write reusable functions and compose modular workflows.
* Exception handling is semantic and reliable, using specific exception classes instead of parsing error strings.

### Key advantages of SDK over CLI for modularity and reusability:

* **Object-oriented responses**: Work with structured data and methods instead of parsing text.
* **Semantic error handling**: Catch and handle exceptions with clear classes.
* **Reusable code**: Build modular functions and workflows that are easier to maintain.

While CLI is simple to get started with, as your automation grows more complex, the SDK’s modularity and semantic features become invaluable for building maintainable and robust CI/CD pipelines.

### Files Are a Headache

When working with CLI-based workflows, managing configuration files (like YAML or JSON) is often a major part of the process. CLI commands typically rely on these files to specify deployment settings, job definitions, or environment configurations.

For example, if you need to deploy to different environments such as **production**, **release**, or **development**, you might have to:

* Maintain separate config files for each environment, following a strict naming convention (e.g., `prod.yml`, `dev.yml`).
* Or dynamically generate these files from templates before each run.

Both approaches add overhead because you need to store, version, and manage these files as pipeline artifacts. This can conflict with the principle of keeping CI/CD runs clean and ephemeral, where ideally no persistent state is carried between runs.

On the other hand, SDK-based workflows tend to avoid heavy reliance on static files. Instead, they build configuration **dynamically in-memory**, using parameters and environment variables passed into the script at runtime.

This offers several benefits:

* You can centralize sensitive or environment-specific values in CI/CD platform features like Azure DevOps Library or GitHub Actions Secrets.
* It reduces the need to generate, track, or maintain separate config files.
* Your pipeline becomes cleaner and easier to manage since configuration lives within the pipeline context and not as separate files.

## 4. Conclusion

Choosing CLI or SDK affects how you build and maintain DevOps workflows. Use **CLI** for quick, simple tasks and easy setup. Use **SDK** for complex, reusable, and maintainable automation with richer logic and better error handling.

If you're skilled with shell scripting, either can work, but SDKs usually scale better as projects grow.

Also, think carefully about your runtime environment—virtual environments, containers, or ephemeral runners—to keep pipelines reliable and clean.

With these points in mind, you can choose the right tool and build more effective DevOps pipelines. Happy code 😎 
