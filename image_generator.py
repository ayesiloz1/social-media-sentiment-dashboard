import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

# Example tweets
raw_tweet = "RT @user: Check out this amazing blog post! https://example.com #awesome #blog 😊"
cleaned_tweet = "Check out this amazing blog post! #awesome #blog"

# 1. Create side-by-side subplots
fig, (ax_left, ax_right) = plt.subplots(ncols=2, figsize=(14, 5))

# 2. Set a white background for the entire figure
fig.patch.set_facecolor('#FFFFFF')

# Turn off the axis lines for both subplots
ax_left.axis('off')
ax_right.axis('off')

# 3. Main (figure-level) title with larger font
fig.suptitle(
    "Tweet Preprocessing: Before & After",
    fontsize=24,        # Larger title
    fontweight='bold',
    color='#2C3E50',    # Darker text
    y=0.97
)

# 4. Left Subplot: Raw Tweet
ax_left.set_facecolor('#FFFFFF')  # White background in the subplot

# Title above the raw tweet
ax_left.text(
    0.5, 0.85,
    "Raw Tweet",
    ha='center', va='center',
    fontsize=16, fontweight='bold', color='#2C3E50',
    transform=ax_left.transAxes
)

# The raw tweet text
raw_text_box = ax_left.text(
    0.5, 0.5,
    raw_tweet,
    ha='center', va='center',
    wrap=True,
    fontsize=13, color='#2C3E50',
    bbox=dict(
        facecolor='#F2D7D5',  # Soft pastel pink
        edgecolor='#D5B5B4',  # Slightly darker edge
        boxstyle='round,pad=0.7'
    ),
    transform=ax_left.transAxes
)

# Add a subtle drop shadow path effect
raw_text_box.set_path_effects([
    path_effects.SimpleLineShadow(offset=(2, -2), shadow_color='#BCAAA4'),
    path_effects.Normal()
])

# 5. Right Subplot: Cleaned Tweet
ax_right.set_facecolor('#FFFFFF')

# Title above the cleaned tweet
ax_right.text(
    0.5, 0.85,
    "Cleaned Tweet",
    ha='center', va='center',
    fontsize=16, fontweight='bold', color='#2C3E50',
    transform=ax_right.transAxes
)

# The cleaned tweet text
clean_text_box = ax_right.text(
    0.5, 0.5,
    cleaned_tweet,
    ha='center', va='center',
    wrap=True,
    fontsize=13, color='#2C3E50',
    bbox=dict(
        facecolor='#E2F0CB',  # Soft pastel green
        edgecolor='#C4DBAA',  # Slightly darker edge
        boxstyle='round,pad=0.7'
    ),
    transform=ax_right.transAxes
)

# Drop shadow effect on the cleaned tweet box
clean_text_box.set_path_effects([
    path_effects.SimpleLineShadow(offset=(2, -2), shadow_color='#B3C49B'),
    path_effects.Normal()
])

# 6. Draw an arrow in the center of the figure to indicate transformation
arrow_x_start = 0.46
arrow_x_end   = 0.54
arrow_y       = 0.55

ax_left.annotate(
    "",
    xy=(arrow_x_end, arrow_y),
    xytext=(arrow_x_start, arrow_y),
    xycoords=fig.transFigure,
    textcoords=fig.transFigure,
    arrowprops=dict(arrowstyle="->", linewidth=3, color="#2C3E50"),
)

# 7. Add a label above the arrow
ax_left.text(
    0.5, arrow_y + 0.03,
    "Data Preprocessing",
    ha='center', va='bottom',
    fontsize=14, fontweight='bold', color='#2C3E50',
    transform=fig.transFigure
)

# Adjust layout and save
plt.tight_layout()
plt.savefig("tweet_preprocessing_visualization.png", bbox_inches="tight")
plt.show()
