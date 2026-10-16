# Section 6 primary-source audit

All method paragraphs, displayed equations, comparison conclusions and semantic caption attributions in main.tex lines 538–739. Read primary-source relevant sections; no replication or code execution claimed.

Coverage: 24 cited methods, 17 displayed equations, 31 audit records.

Most consequential correction: TimeCAP must convert the LLM class to one-hot before mixing with multimodal logits. Other changes clarify evidence availability and notation, rather than inventing missing mechanisms.

## forecast_contract — pass

Manuscript lines 540–550; primary PDF pages [].

Survey-authored definition of forecasting information and horizon; future-known calendar covariates are permitted by information availability at the origin.

- `eq:forecast-contract`: survey_definition; source None; pass. Not attributed to an individual method; no false claim of author derivation.

## timeseriesscientist2025 — pass_with_clarification

Manuscript lines 566–576; primary PDF pages [5, 6].

Sections 3.3–3.4, Eq. (2)–(3): validation MAPE selects each candidate configuration, and Forecaster fixes ensemble strategy and weights before touching the test split.

- `eq:tsci-planner`: author_equations; source (2), (3); pass. Objective direction, candidate set, denominator and processed validation set agree. MAPE is undefined for zero target values in this displayed form, as in source; avoid presenting it as universally suitable.

**P2 — Make the useful train/test distinction explicit in the existing method paragraph.**

The selected configurations are ranked, and the Forecaster uses their validation results to choose a single model or an ensemble, fixing its strategy and weights before evaluating the test set.

## timecopilot2025 — pass

Manuscript lines 576–576; primary PDF pages [2, 3].

Sections 2–2.2: feature analysis, candidate proposal and cross-validation, final forecasting; unified API exposes statistical, ML, DL and foundation forecasters. Current short comparison is supported.

## flairr2025 — revise

Manuscript lines 578–589; primary PDF pages [2, 3].

Algorithm 1 includes recent ground truth X[t:t+H] among required inputs. It returns current prompt on early stop and best observed-MAE prompt when reaching iteration limit. The deployment scheduling statement is survey guidance, not demonstrated online protocol.

- `eq:flairr-loop`: algorithm_restatement; source Algorithm 1; revise. Copies source inclusive t:t+H notation, which implies H+1 points under ordinary inclusive indexing; clashes with declared H-point horizon. MAE is positive and minimized correctly.

**P2 — Normalize the evaluation window without propagating the source indexing ambiguity; distinguish retrospective feedback from unresolved forecast.**

Use a resolved validation window $V=(t_1,\ldots,t_H)$ in Eq.~\ref{eq:flairr-loop}, replacing $X_{t:t+H}$ by $X_V$. Follow the equation with: "Here $X_V$ is the observed target sequence for an $H$-step refinement window. The refiner proposes prompt updates from earlier prompts and errors; early stopping returns the current prompt, while reaching the iteration limit returns the lowest-MAE prompt. In deployment, this feedback becomes available when the refinement window has resolved."

## castfsr2026 — revise

Manuscript lines 591–606; primary PDF pages [3, 4].

Eqs. (1)–(8): I=(D_task,D_domain,X_1:L,H_ctx); M is running memory, W adaptive context lookback. Context, candidate generation, reflection and final forecast exactly correspond to source.

- `eq:castfsr-state-action`: equivalent_restatement; source (1)–(3); pass. Adds step k consistently to prior and context.

- `eq:castfsr-revision`: equivalent_restatement; source (4)–(8); pass. Source functions and arguments retained; symbols currently underdefined.

**P2 — Define method-local symbols and replace classification justification with reader-facing explanation.**

Here $I=(D_{\mathrm{task}},D_{\mathrm{domain}},X_{1:L},H_{\mathrm{ctx}})$ contains the target and horizon, domain description, observed series, and available contextual history; $M_k$ stores the interaction history and $W_k$ sets the context lookback. Reflection checks the candidate against temporal alignment, contextual support, and domain constraints such as units and capacity. Weak or redundant context can leave the numerical prior unchanged, whereas relevant evidence supports a targeted revision.

## lastmile2026 — pass

Manuscript lines 606–606; primary PDF pages [4, 5].

Baseline forecast workspace, constrained event-window revision, then reflection after actual values arrive. Current contextual revision claim supported.

## castflow2026 — pass

Manuscript lines 606–606; primary PDF pages [4].

Planning/action/forecasting/reflection loop; frozen planner and tuned forecasting model refine numerical baseline from toolkit evidence.

## hydroagent2026 — pass

Manuscript lines 606–606; primary PDF pages [7].

Hydrological model workflow includes prior judgment, flood type selection, rolling forecast and bulletin publication; LLM coordinates while tools simulate.

## scenariodiff2026 — revise

Manuscript lines 608–616; primary PDF pages [3, 4, 5].

Forward noising Eq. (3), clean-horizon reconstruction loss Eq. (6), historical/scenario conditions and Anchor Blended Sampling Alg. 2. Historical inputs include numerical lookback; scenario generated from history. Anchor editing occurs after initial forecast, retaining non-anchor regions.

- `eq:scenariodiff-denoising`: author_equations; source (3), (6); pass. Correct x0 reconstruction, not epsilon prediction. t is diffusion step, not observational time.

**P2 — Define all conditioning inputs and distinguish diffusion steps from observation time.**

Here $x^{(0)}$ is the future target horizon, $t$ indexes diffusion steps, $\epsilon\sim\mathcal{N}(0,I)$, and $c$ contains the numerical lookback, historical-text summary, and a scenario inferred from historical information. Anchor Blended Sampling edits anchor-relevant regions of the generated trajectory while retaining the remaining temporal structure.

## timecap2025 — revise

Manuscript lines 618–630; primary PDF pages [3, 4, 5].

Section 3.3 Eq. (1)–(3): training-set nearest-neighbour descriptions and labels; discrete LLM class converted to one-hot before fusion with encoder logits. F1/AUROC evaluates event classification, not probability calibration.

- `eq:timecap-retrieval`: author_equations; source (1), (2); pass. Nearest-neighbour domain must explicitly be training set.

- `eq:timecap-dual-agent`: equivalent_restatement; source (3) and unnumbered fused prediction; revise. Missing one-hot conversion creates incompatible scalar-label/vector-logit types.

**P1 — Correct the fusion types rather than treating the LLM class as a calibrated probability.**

Replace the fusion display by $\widehat c_{\mathrm{LLM}}=A_P(s_x,\mathcal S),\quad \widehat y=\lambda\,\operatorname{onehot}(\widehat c_{\mathrm{LLM}})+(1-\lambda)\widehat y_{\mathrm{MM}}$. Precede it with: "The retrieved training-set descriptions and labels serve as in-context examples. The predictor returns a discrete event class, which is converted to a one-hot vector and combined with the encoder logits, with $\lambda\in[0,1]$."

## aiaforecaster2025 — pass

Manuscript lines 630–630; primary PDF pages [8, 9, 10].

Section 3.2: independent agentic search; supervisor searches to resolve disagreement before aggregation; Platt scaling corrects final probability. Current prose supported.

## auditforecast2026 — pass

Manuscript lines 630–630; primary PDF pages [3, 4].

Section 3 and Fig.2: quantitative model-derived baseline and situational-factor odds updates; factors vetted for baseline scope and independence. Current prose supported.

## forecasting_synthesis — pass

Manuscript lines 630–630; primary PDF pages [].

The conclusion contrasts trajectory error with resolved event probabilities, evidence access and calibration. This is survey-authored selection guidance; does not assert every method measures every property.

## bridge2025 — pass

Manuscript lines 636–642; primary PDF pages [3, 4, 5].

Section 3 defines f_theta(D,l,z)->xhat. Section 4.1 uses text-conditioned forecasting to refine templates; Section 4.2 conditions diffusion on text and domain prototypes. Refined templates fixed before subsequent dataset construction; two construction datasets versus twelve disjoint generation datasets.

- `eq:bridge-generation`: author_formulation; source Section 3 unnumbered mapping; pass. Accurate functional definition, not a training loss.

## merit2025 — pass

Manuscript lines 644–644; primary PDF pages [3, 4, 5].

Fig.2 and Sections 3.2–3.5: similarity retrieval followed by LLM filtering, library-based augmentation, review approves positive views into memory or repeats; views and neighbours support contrastive learning. Figure attribution to Fig.2 correct.

## metacaster2026 — revise

Manuscript lines 646–657; primary PDF pages [3, 4, 5, 6].

Eqs.(1),(2),(4) and Sections 3.3–3.7 match. Omega uses optimization-corpus internal test splits as harness-training feedback. Final evaluation uses seven IND and three OOD datasets disjoint from eight-dataset harness training corpus. Proposer discarded after optimization.

- `eq:metacaster-objective`: equivalent_restatement; source (1), (2); pass. Argmin restates source min; theta is prompt/skill harness, not LLM weights.

- `eq:metacaster-hinge`: author_equation; source (4); pass. Direction and denominator match; positive baseline forecast error assumed.

**P2 — Clarify what is optimized and what constitutes held-out evaluation within the method explanation.**

Here $\theta$ denotes the generator's prompt and skills, and $\omega$ measures forecasting error on the evaluation split of a dataset in the harness-optimization corpus. This feedback updates the generator; final generalization is assessed on separate in-domain and out-of-domain datasets. After optimization, the Harness Proposer is removed and the learned prompts and skills guide generation for the new support set.

## chatad2026 — pass

Manuscript lines 659–659; primary PDF pages [2, 3, 4].

TSEvol explicitly separates Consultant–Client Cognitive Reasoning Layer from Supervisor–Intern Interactive Feedback Layer. The manuscript locates agent use in instruction construction, not deployment, consistent with source.

## synthesis_comparison — pass

Manuscript lines 634–634; primary PDF pages [].

Generated object and intended learner are valid comparison criteria; the paragraphs at lines659–661 distinguish representation-learning views, downstream forecast training, and LLM instruction dialogues. No unsupported claim of universal efficacy.

## synthesis_closure — pass

Manuscript lines 661–661; primary PDF pages [].

MERIT review determines accepted views; MetaCaster outer optimization uses forecast error. Selecting based on learner and available feedback is a survey interpretation grounded in those mechanisms.

## anomamind2026 — revise

Manuscript lines 674–687; primary PDF pages [4, 5, 6].

Eqs.(5),(6),(7),(8) reproduced correctly. Diagnostic state s_k=(S^(k),Z_1:k,C_1:k), whereas source also uses s_j for a candidate interval. Training uses labeled parsing/F1/FP rewards; only detector policy is trained, not full workflow.

- `eq:anomamind-decision`: author_equations; source (5), (6); pass. Mathematically source-faithful but state/interval s collision must be explained or renamed.

- `eq:anomamind-reward`: author_equations; source (7), (8); pass. Max direction and FP minus sign correct; feedback requires training labels.

**P2 — Make candidate interval distinct from agent state and name reward availability.**

Write the detector as $\widehat y_j=D_\theta(u_j,Z_{1:k},C_{1:k})$ and define $u_j=[\ell_j,r_j]$ as a candidate interval, while $s_k=(S^{(k)},Z_{1:k},C_{1:k})$ is the diagnostic state. Replace the reward introduction by: "During detector training, rule-based feedback combines parse validity, agreement with labeled anomalous intervals, and a false-positive penalty."

## sagead2026 — pass

Manuscript lines 689–689; primary PDF pages [3, 4, 5, 15].

Section 3: original series retained for tools, compressed summaries for LLM; family analyzers; confidence/type/interval output; reference pool excludes labeled anomalies, k-medoids prototypes perturbed into nine types. No real anomalous examples or test labels used in that pool construction. Manuscript supported.

## argos2025 — pass

Manuscript lines 691–691; primary PDF pages [5, 6].

Detection generates rules; Repair executes dummy inputs; Review checks validation accuracy and may revert regressions; deployment fuses with base detector. Current description and training/deployment distinction supported.

## adagent2025 — revise

Manuscript lines 693–693; primary PDF pages [2, 3, 4].

Processor/Selector/Info Miner/Code Generator/Reviewer sequence and TSLib branch match. Reviewer performs dry run on synthetic samples. Evaluator/Optimizer are optional and source emphasizes pipeline success/cost, with additional model-selection evaluation.

**P2 — Current "Evaluation then pairs execution checks with detection metrics on held-out series" sounds like a verified source protocol; explicitly distinguish optional source evaluation from recommended held-out evaluation.**

Its Reviewer tests execution on synthetic samples; optional Evaluator and Optimizer agents assess labeled data and tune hyperparameters. For a deployed time-series pipeline, executable-code success and detection performance on held-out series provide complementary checks.

## ji2025lemad — pass

Manuscript lines 695–695; primary PDF pages [5, 6, 11].

Section 3.1 source workflow is almost verbatim: metrics/logs via Kafka, real-time correlation, alert summaries, preliminary hypotheses, anomaly diagnosis confidence/root-cause/recommendations. Section 4.3 explicitly defines precision/recall/F1/latency.

## anomaly_comparison — pass

Manuscript lines 672–695; primary PDF pages [].

Contrasts interval detection versus diagnosis artifacts, learned evidence acquisition versus retrieved examples versus assembled pipelines. These are survey judgments anchored in the verified method descriptions. No extrapolated score claim.

## finmem2023 — pass

Manuscript lines 707–707; primary PDF pages [3, 6, 7, 8, 9].

Section 3.2: event recency/relevance/importance, shallow/intermediate/deep lifetimes; important memories transition deeper. Training sees next-day price ground labels, testing does not; manuscript currently claims only memory mechanism and current-market-conditioned decisions.

## fincon2024 — revise

Manuscript lines 709–724; primary PDF pages [3, 4, 5].

Source Eq.(1) portfolio weights and Eq.(2) cumulative PnL match. Hold = zero, sell = short, weights rebalanced daily. Within-episode risk feedback used during test; over-episode prompt changes training only.

- `eq:fincon-objective`: author_equation; source (2); pass. theta textual prompts, alpha discount; O observation/B self-reflection/A trading action currently undefined.

- `eq:fincon-portfolio`: author_equation; source (1); pass. mu/Sigma are shrinkage estimates of mean daily returns/covariance; source objective has implicit fixed risk tradeoff, not learned risk aversion.

**P2 — Define quantities and explain training/deployment meaning of prompt-controlled objective.**

Here $\theta$ comprises agent prompts, $\alpha$ discounts future rewards, and $O_t$, $B_t$, and $A_t$ denote market observations, managerial reflection, and trading action. FinCon updates prompts between training episodes from comparative performance feedback; within-episode risk alerts also guide testing decisions. In the allocation problem, $\mu$ and $\Sigma$ are shrinkage estimates of mean daily returns and their covariance.

## tradingagents2024 — pass

Manuscript lines 724–724; primary PDF pages [6, 7, 9].

Analyst reports feed bullish/bearish researcher debate, then trader action and risk-management discussion; source structured state and role sequence support manuscript comparison.

## collmllight2026 — pass_with_clarification

Manuscript lines 726–737; primary PDF pages [3, 4, 5].

Source Eqs.(3),(4),(5) exactly match history, prompt and action equations. Section 3.2 reduces full reasoning based on critical-neighbour congestion count. Section 3.3 simulator trajectories support supervised policy training and feedback refinement.

- `eq:collmlight-state`: author_equations; source (3), (4); pass. Open time-window boundaries agree with source.

- `eq:collmlight-action`: author_equation; source (5); pass. Full reasoning mode; simple/no-cooperation modes omit future-state prediction.

**P2 — Name that the displayed full prediction-to-action sequence is selected for complex coordination.**

For complex coordination, the LLM analyzes current traffic, predicts neighboring states under candidate configurations, and selects a signal. Simpler situations omit some of these reasoning stages according to the number of critical neighboring lanes.

## decision_comparison — pass

Manuscript lines 737–739; primary PDF pages [].

Contrasts predictive evidence with feasible actions, state, reward timing and utility; reasonable survey synthesis based on portfolio and traffic methods. No claim that prediction accuracy establishes action value.

## figures — pass_with_scope_note

Manuscript lines 552–702; primary PDF pages [].

Task-family diagram is explicitly survey-authored adaptation. MERIT Fig.2 attribution matches original workflow; AnomaMind workflow and role stages match original Fig.1/Sections IV.B–D. This audit verified semantic caption provenance, not visual rendering or editable PPT fidelity.
