import matplotlib.pyplot as plt

threads = [1, 2, 4, 6, 8]
serial = [120.753, 122.310, 122.662, 120.832, 121.153]
ispc = [39.744, 39.892, 39.927, 40.707, 40.768]
multi_ispc = [20.090, 21.455, 22.695, 22.777, 20.591]

avg_serial = sum(serial) / len(serial)
speedup_ispc = [avg_serial / s for s in ispc]
speedup_multi = [avg_serial / s for s in multi_ispc]

# ===== 图1 =====
fig, ax = plt.subplots(figsize=(6, 4.5))
w = 0.3
ax.bar(
    [t - w / 2 for t in threads],
    speedup_ispc,
    w,
    label="ISPC (Single Core)",
    color="#3498db",
)
ax.bar(
    [t + w / 2 for t in threads],
    speedup_multi,
    w,
    label="Tasks + ISPC (Multi Core)",
    color="#e74c3c",
)
for i, t in enumerate(threads):
    ax.text(
        t - w / 2,
        speedup_ispc[i] + 0.08,
        f"{speedup_ispc[i]:.1f}x",
        ha="center",
        fontsize=8,
    )
    ax.text(
        t + w / 2,
        speedup_multi[i] + 0.08,
        f"{speedup_multi[i]:.1f}x",
        ha="center",
        fontsize=8,
    )
ax.axhline(
    y=4.0,
    color="gray",
    linestyle="--",
    linewidth=0.8,
    alpha=0.6,
    label="NEON Theoretical (4x)",
)
ax.axhline(
    y=1.0,
    color="#2ecc71",
    linestyle=":",
    linewidth=1.2,
    alpha=0.7,
    label="Serial Baseline (1x)",
)
ax.set_xlabel("Number of Tasks", fontsize=8)
ax.set_ylabel("Speedup (vs. Serial)", fontsize=8)
ax.set_xticks(threads)
ax.grid(axis="y", alpha=0.3)
ax.set_ylim(0, 7)
# 图例放在图表上方，右对齐；通过调整bbox和tight_layout防止遮挡和截断
ax.legend(fontsize=5, loc="upper right", bbox_to_anchor=(1.0, 1.12))
fig.tight_layout(rect=[0, 0, 1, 0.85])
plt.savefig("fig1_speedup.png", dpi=200, bbox_inches="tight")
plt.close()

# ===== 图2 =====
fig2, ax2 = plt.subplots(figsize=(6, 4.5))
ax2.plot(threads, multi_ispc, "ro-", linewidth=2, markersize=5, label="Tasks + ISPC")
ax2.axhline(
    y=multi_ispc[0],
    color="#3498db",
    linestyle="--",
    linewidth=1,
    alpha=0.7,
    label=f"Baseline t=1 ({multi_ispc[0]:.1f} ms)",
)
for i, t in enumerate(threads):
    offset_y = 8 if i != 3 else -15
    ax2.annotate(
        f"{multi_ispc[i]:.1f} ms",
        (t, multi_ispc[i]),
        textcoords="offset points",
        xytext=(8, offset_y),
        fontsize=9,
    )
ax2.set_xlabel("Number of Tasks", fontsize=8)
ax2.set_ylabel("Execution Time (ms)", fontsize=8)
ax2.set_xticks(threads)
ax2.grid(alpha=0.3)
ax2.set_ylim(18, 25)
# 图例放在图表上方，右对齐
ax2.legend(fontsize=5, loc="upper right", bbox_to_anchor=(1.0, 1.12))
fig2.tight_layout(rect=[0, 0, 1, 0.85])
plt.savefig("fig2_scalability.png", dpi=200, bbox_inches="tight")
plt.close()

