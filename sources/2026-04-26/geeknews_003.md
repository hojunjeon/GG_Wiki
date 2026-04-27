---
source: geeknews
date: 2026-04-26
points: 11
url: "https://github.com/SWE-agent/mini-swe-agent"
title: mini-swe-agent - 100줄짜리 AI 에이전트로 GitHub 이슈 해결 및 커맨드라인 지원
---

# mini-swe-agent - 100줄짜리 AI 에이전트로 GitHub 이슈 해결 및 커맨드라인 지원

📣 New tutorial on building minimal AI agents
📣 Gemini 3 Pro reaches 74% on SWE-bench verified with mini-swe-agent!
📣 New blogpost: Randomly switching between GPT-5 and Sonnet 4 boosts performance
Warning
This is mini-swe-agent v2. Read the migration guide. For the previous version, check out the v1 branch.
In 2024, we built SWE-bench & SWE-agent and helped kickstart the coding agent revolution.
We now ask: What if our agent was 100x simpler, and still worked nearly as well?
mini
is
- Widely adopted: Used by Meta, NVIDIA, Essential AI, IBM, Nebius, Anyscale, Princeton University, Stanford University, and many more.
- Minimal: Just some 100 lines of python for the agent class (and a bit more for the environment, model, and run script) — no fancy dependencies!
- Performant: Scores >74% on the SWE-bench verified benchmark; starts much faster than Claude Code
- Deployable: Supports local environments, docker/podman, singularity/apptainer, bublewrap, contree, and more
- Compatible: Supports all models via litellm, openrouter, portkey, and more. Support for
/completion
and/response
endpoints, interleaved thinking etc. - Built by the Princeton & Stanford team behind SWE-bench, SWE-agent, and more
- Tested:
More motivation (for research)
SWE-agent jump-started the development of AI agents in 2024. Back then, we placed a lot of emphasis on tools and special interfaces for the agent.
However, one year later, as LMs have become more capable, a lot of this is not needed at all to build a useful agent!
In fact, the mini
agent
- Does not have any tools other than bash — it doesn't even need to use the tool-calling interface of the LMs. This means that you can run it with literally any model. When running in sandboxed environments you also don't need to take care of installing a single package — all it needs is bash.
- Has a completely linear history — every step of the agent just appends to the messages and that's it. So there's no difference between the trajectory and the messages that you pass on to the LM. Great for debugging & fine-tuning.
- Executes actions with
subprocess.run
— every action is completely independent (as opposed to keeping a stateful shell session running). This makes it trivial to execute the actions in sandboxes (literally just switch outsubprocess.run
withdocker exec
) and to scale up effortlessly. Seriously, this is a big deal, trust me.
This makes it perfect as a baseline system and for a system that puts the language model (rather than
the agent scaffold) in the middle of our attention.
You can see the result on the SWE-bench (bash only) leaderboard, that evaluates the performance of different LMs with mini
.
More motivation (as a tool)
Some agents are overfitted research artifacts. Others are UI-heavy frontend monsters.
The mini
agent wants to be a hackable tool, not a black box.
- Simple enough to understand at a glance
- Convenient enough to use in daily workflows
- Flexible to extend
Unlike other agents (including our own swe-agent), it is radically simpler, because it:
- Does not have any tools other than bash — it doesn't even need to use the tool-calling interface of the LMs. Instead of implementing custom tools for every specific thing the agent might want to do, the focus is fully on the LM utilizing the shell to its full potential. Want it to do something specific like opening a PR? Just tell the LM to figure it out rather than spending time to implement it in the agent.
- Executes actions with
subprocess.run
— every action is completely independent (as opposed to keeping a stateful shell session running). This is a big deal for the stability of the agent, trust me. - Has a completely linear history — every step of the agent just appends to the messages that are passed to the LM in the next step and that's it. This is great for debugging and understanding what the LM is prompted with.
Should I use SWE-agent or mini-SWE-agent?
You should consider mini-swe-agent
your default choice.
In particular, you should use mini-swe-agent
if
- You want a quick command line tool that works locally
- You want an agent with a very simple control flow
- You want even faster, simpler & more stable sandboxing & benchmark evaluations
- You are doing FT or RL and don't want to overfit to a specific agent scaffold
You should use swe-agent
if
- You want to experiment with different sets of tools, each with their own interface
- You want to experiment with different history processors
What you get with both
- Excellent performance on SWE-Bench
- A trajectory browser
Option 1: If you just want to try out the CLI (package installed in anonymous virtual environment)
pip install uv && uvx mini-swe-agent
# or
pip install pipx && pipx ensurepath && pipx run mini-swe-agent
Option 2: Install CLI & python bindings in current environment
pip install mini-swe-agent
mini # run the CLI
Option 3: Install from source (developer setup)
git clone https://github.com/SWE-agent/mini-swe-agent.git
cd mini-swe-agent && pip install -e .
mini # run the CLI
Read more in our documentation:
- Quick start guide
- Using the
mini
CLI - Global configuration
- Yaml configuration files
- Power up with the cookbook
- FAQ
- Contribute!
If you found this work helpful, please consider citing the SWE-agent paper in your work:
@inproceedings{yang2024sweagent,
title={{SWE}-agent: Agent-Computer Interfaces Enable Automated Software Engineering},
author={John Yang and Carlos E Jimenez and Alexander Wettig and Kilian Lieret and Shunyu Yao and Karthik R Narasimhan and Ofir Press},
booktitle={The Thirty-eighth Annual Conference on Neural Information Processing Systems},
year={2024},
url={https://arxiv.org/abs/2405.15793}
}
Our other projects: