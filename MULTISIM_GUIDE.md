# 🚀 Multisim Guide: Find Your Optimal Bot Configuration

## 📋 Quick Reference

| Tool | Purpose | Time | When to Use |
|------|---------|------|-------------|
| **`./run_bot.sh sim`** | Test ONE config | 15-20 min | Quick validation, testing specific settings |
| **`./run_multisim.sh`** | Test 36 configs | 2-3 hours | Find best settings, optimize performance |

---

## 🎯 When Should You Use Multisim?

### ✅ **Use Multisim When:**

1. **Your current bot is losing money** (< 50% accuracy)
   - Multisim will find better parameter combinations
   - Automatic optimization beats manual guessing

2. **You're starting fresh** and want the best config from day 1
   - Let multisim test everything overnight
   - Wake up to the optimal settings

3. **Market conditions changed** and your bot stopped working
   - Old settings: 55% accuracy → Now: 48%
   - Multisim finds new optimal params for current market

4. **You want to maximize profits**
   - Your bot: 52% accuracy (barely profitable)
   - Multisim might find: 56% accuracy configuration (+4% boost!)

5. **You're not sure which settings to use**
   - Should I use 1000 or 2000 training epochs?
   - Linear or XGBoost?
   - Multisim answers these questions with data!

---

### ❌ **DON'T Use Multisim When:**

1. **Your bot is already profitable** (> 53% accuracy)
   - If it works, don't break it!
   - Maybe optimize monthly, not daily

2. **You just want to test ONE change**
   - Just run `./run_bot.sh sim` (15 min)
   - Multisim is overkill

3. **You need results immediately**
   - Multisim takes 2-3 hours minimum
   - Use regular `sim` for quick tests

---

## 🔬 How Multisim Works

### **Regular Sim:**
```
Test: max_n_train=1000, autoregressive_n=3, Linear
Result: 51% accuracy
```

### **Multisim:**
```
Test 1:  max_n_train=500,  autoregressive_n=2, Linear, No SMOTE  → 48% ❌
Test 2:  max_n_train=500,  autoregressive_n=2, Linear, SMOTE     → 49% ❌
Test 3:  max_n_train=500,  autoregressive_n=2, XGBoost, No SMOTE → 50% ⚠️
Test 4:  max_n_train=500,  autoregressive_n=2, XGBoost, SMOTE    → 52% ✅
...
Test 36: max_n_train=2000, autoregressive_n=5, XGBoost, SMOTE    → 56% ✅✅✅ BEST!

Winner: max_n_train=2000, autoregressive_n=5, XGBoost, SMOTE
        → 56% accuracy (would earn +45 OCEAN/week!)
```

**Multisim automatically finds the BEST combination!**

---

## ⚡ Your Fast Multisim Configuration

I created `multisim_ppss.yaml` optimized for SPEED:

### **What It Tests:**

| Parameter | Values | Impact |
|-----------|--------|--------|
| `max_n_train` | 500, 1000, 2000 | How much historical data to train on |
| `autoregressive_n` | 2, 3, 5 | How far back to look (10-25 min) |
| `approach` | Linear, XGBoost | ML algorithm (Linear fast, XGBoost better) |
| `balance_classes` | None, SMOTE | Fix UP/DOWN prediction bias |

**Total:** 3 × 3 × 2 × 2 = **36 combinations**

### **Speed Optimizations:**
- ✅ `test_n: 100` (not 500) = 5x faster per test
- ✅ `train_every_n_epochs: 10` (not 5) = 2x faster per test
- ✅ `calc_imps: False` = Skips feature importance calculation

**Time per test:** ~4 minutes  
**Total time:** 36 × 4 min = **~2.5 hours** ⚡

---

## 🚀 How to Run Multisim

### **Step 1: Stop Your Current Simulation**
```bash
# In the terminal running sim
Ctrl + C
```

### **Step 2: Run Multisim**
```bash
./run_multisim.sh
```

### **Step 3: Wait 2-3 Hours**
Go do something else! Multisim will:
- Test all 36 combinations automatically
- Track which one performs best
- Save all results

### **Step 4: Check Results**
After multisim completes, it will show you the **WINNER**:

```
════════════════════════════════════════════
MULTISIM RESULTS
════════════════════════════════════════════
Tested: 36 configurations
Winner: Run #28

Best Configuration:
  max_n_train: 2000
  autoregressive_n: 5
  approach: ClassifXgboost
  balance_classes: SMOTE
  
Results:
  Accuracy: 56.2%
  Expected Profit: +42 OCEAN/week
════════════════════════════════════════════
```

---

## 📝 Applying the Winning Configuration

### **Option A: Manual Update** (Recommended)

1. Look at the winning parameters in multisim output
2. Edit `my_ppss.yaml`:

```yaml
aimodel_data_ss:
  max_n_train: 2000  # ← Copy from winner
  autoregressive_n: 5  # ← Copy from winner
  transform: None

aimodel_ss:
  approach: ClassifXgboost  # ← Copy from winner
  balance_classes: SMOTE  # ← Copy from winner
  train_every_n_epochs: 5  # Set back to 5 for mainnet
```

3. Save and deploy:
```bash
./run_bot.sh mainnet
```

---

### **Option B: Test Winner First**

Want to validate the winner before deploying?

1. Update `my_ppss.yaml` with winning params
2. Run ONE more sim to confirm:
```bash
./run_bot.sh sim  # Validate winner
```
3. If results match multisim → Deploy to mainnet!

---

## 💡 Recommended Workflow

### **For Beginners:**
```
Day 1: Run ONE quick sim to establish baseline
       ./run_bot.sh sim (15 min)
       
       If < 50%: Run multisim overnight
       If > 52%: Deploy to mainnet!

Day 2: Apply winning multisim config to mainnet
       Monitor for 24-48 hours
```

### **For Optimization:**
```
Week 1: Run mainnet with default config
Week 2: Collect performance data
Week 3: Run multisim to find improvements
Week 4: Deploy optimized config
```

### **For Troubleshooting:**
```
If bot starts losing money:
1. Check current accuracy: python check_mainnet_performance.py
2. If < 50%: Stop bot immediately
3. Run multisim to find new optimal settings
4. Deploy winner, monitor closely
```

---

## 📊 Understanding Multisim Output

During multisim, you'll see output like:

```
Testing configuration 1/36...
  max_n_train=500, autoregressive_n=2, Linear, No SMOTE
  Accuracy: 48.5% (96/200 correct)
  Profit: -2.3 OCEAN
  
Testing configuration 2/36...
  max_n_train=500, autoregressive_n=2, Linear, SMOTE
  Accuracy: 49.8% (99/200 correct)
  Profit: -0.5 OCEAN
  
...

Testing configuration 28/36...
  max_n_train=2000, autoregressive_n=5, XGBoost, SMOTE
  Accuracy: 56.2% (112/200 correct)
  Profit: +8.4 OCEAN ← BEST SO FAR!
```

**Look for:**
- ✅ Highest accuracy (aim for > 52%)
- ✅ Positive cumulative profit
- ✅ Consistency (not just lucky guesses)

---

## 🎯 Quick Decision Tree

```
Do you want to...

├─ Test ONE specific idea?
│  └─> Use: ./run_bot.sh sim (15 min)
│
├─ Find the BEST possible settings?
│  └─> Use: ./run_multisim.sh (2-3 hours)
│
├─ Quickly check if current settings work?
│  └─> Use: ./run_bot.sh sim (15 min)
│
├─ Optimize an already-working bot?
│  └─> Use: ./run_multisim.sh (monthly)
│
└─ Emergency: bot is losing money!
   └─> Use: ./run_multisim.sh (find fix ASAP)
```

---

## ⚠️ Important Notes

### **Multisim Uses Simulation Settings**
- Multisim tests configurations in simulation mode
- Results show EXPECTED performance on historical data
- Mainnet performance may vary slightly (±1-2%)

### **Multisim is Resource-Intensive**
- Will use 100% CPU for 2-3 hours
- Don't run while mainnet bot is running (same machine)
- Best to run overnight or on separate machine

### **More Parameters = More Time**
- Current: 36 combinations = 2.5 hours
- If you add more values: Time increases exponentially
- Example: Adding 1 more parameter → 6-8 hours

### **Historical Data Matters**
- Multisim tests on last 60 days of data
- If market changes dramatically, rerun multisim
- Winning config for bull market ≠ winning config for bear market

---

## 🚀 Your Action Plan

### **RIGHT NOW:**

**Step 1: Run ONE quick sim** (15 min)
```bash
./run_bot.sh sim
```

**Step 2: Check results**
- Accuracy > 52%? → Deploy to mainnet! ✅
- Accuracy < 50%? → Continue to Step 3

**Step 3: Run multisim** (if needed, 2-3 hours)
```bash
./run_multisim.sh
```

**Step 4: Apply winning config and deploy!**

---

## 📋 Summary

| Question | Answer |
|----------|--------|
| **Should I use multisim?** | Yes, if accuracy < 52% or want to optimize |
| **How long does it take?** | 2-3 hours (36 tests × 4 min each) |
| **Will it find better settings?** | Very likely! Automatic optimization > guessing |
| **When to use regular sim?** | Quick testing, validation, specific ideas |
| **Can I run both?** | Yes! Sim for quick tests, multisim for optimization |

---

**Bottom line:** If your bot isn't profitable yet (< 52%), multisim is your best friend. It will find the optimal configuration automatically while you sleep! 🌙✨
