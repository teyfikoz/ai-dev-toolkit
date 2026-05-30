# NVIDIA NIM & NeMo Ekosistemi

NVIDIA'nın AI model deployment, inference ve retrieval altyapısı.

> **Not — NIM API Erişimi:** build.nvidia.com API'si Türkiye telefon numarasıyla doğrulama desteklemiyor.
> Alternatifler: **Groq** (ücretsiz, hızlı, Llama3/Mixtral, ülke kısıtı yok) veya **Together.AI**, **Fireworks.AI**.
> Öz-barındırma için aşağıdaki nim-anywhere/nim-deploy repoları GPU gerektiriyor.

| # | Repo | Stars | Ne İşe Yarar? | GitHub |
|---|------|-------|--------------|--------|
| 1 | **nim-anywhere** | 550 | NIM modellerini kendi altyapında barındırma: Docker Compose + GPU ortamı kurulum şablonları | [link](https://github.com/NVIDIA/nim-anywhere) |
| 2 | **nim-deploy** | 420 | NIM container'larını production'a dağıtma rehberleri (Docker, Helm, Kubernetes) | [link](https://github.com/NVIDIA/nim-deploy) |
| 3 | **k8s-nim-operator** | 340 | Kubernetes üzerinde NIM deployment'larını yöneten Kubernetes Operator | [link](https://github.com/NVIDIA/k8s-nim-operator) |
| 4 | **workbench-example-downloadable-nim** | 120 | NVIDIA AI Workbench ile yerel NIM indirme ve çalıştırma örneği | [link](https://github.com/NVIDIA/workbench-example-downloadable-nim) |
| 5 | **rag (AI Blueprints)** | 350 | NVIDIA NIM ile kurumsal RAG referans mimarisi — embedding + retrieval + generation pipeline | [link](https://github.com/NVIDIA-AI-Blueprints/rag) |
| 6 | **NeMo-Retriever** | 320 | NVIDIA NeMo tabanlı retrieval sistemi — dense + sparse hibrit arama, reranking | [link](https://github.com/NVIDIA/NeMo-Retriever) |
