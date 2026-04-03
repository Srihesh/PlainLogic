# Gemini Follow-up Sanity Checks

Fri Apr  3 18:44:34 IST 2026

## 1) Tokenless heuristic run from script path
EXIT: 0
      "total_reward": 0.48,
      "final_score": 1.0
    },
    {
      "task": "medium",
      "seed": 7,
      "steps": 12,
      "total_reward": 1.54,
      "final_score": 1.0
    },
    {
      "task": "hard",
      "seed": 7,
      "steps": 18,
      "total_reward": 2.24,
      "final_score": 1.0
    }
  ],
  "aggregate_score": 1.0
}

## 2) Tokenless heuristic run from outside repo
EXIT: 0
      "total_reward": 0.48,
      "final_score": 1.0
    },
    {
      "task": "medium",
      "seed": 7,
      "steps": 12,
      "total_reward": 1.54,
      "final_score": 1.0
    },
    {
      "task": "hard",
      "seed": 7,
      "steps": 18,
      "total_reward": 2.24,
      "final_score": 1.0
    }
  ],
  "aggregate_score": 1.0
}

## 3) Model mode without token should fail fast
EXIT: 1
Missing API token. Set one of: OPENAI_API_KEY, HF_TOKEN, HUGGINGFACEHUB_API_TOKEN, HF_API_TOKEN
Hackathon path: use HF_TOKEN with OPENAI_BASE_URL=https://router.huggingface.co/v1
Tip: create .env from .env.example and run this script again

## 4) Regression tests
..........                                                               [100%]
10 passed in 0.13s
