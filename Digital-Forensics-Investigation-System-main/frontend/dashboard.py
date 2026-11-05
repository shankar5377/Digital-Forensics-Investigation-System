import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from backend.case_service import (
    get_cases_by_status,
    get_cases_by_type,
    get_recent_cases,
)
from backend.evidence_service import get_recent_evidence
from backend.user_service import get_stat_counts

BG_DARK = "#f3f5fa"
BG_CARD = "#ffffff"
BG_CARD_ALT = "#f5f7fc"
PURPLE = "#4f46e5"
PURPLE2 = "#7c3aed"
TEXT_MAIN = "#172033"
TEXT_DIM = "#596579"
TEXT_FAINT = "#8290a5"
SEP_COLOR = "#e4e9f2"
GREEN = "#22c55e"
RED = "#dc3545"
ORANGE = "#d97706"
BLUE = "#2563eb"

class DashboardFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, session, **kwargs):
        super().__init__(master, **kwargs)
        self.session = session
        self.configure(fg_color=BG_DARK, scrollbar_button_color="#d5dce8")
        self._build()

    def _build(self):
        self._build_header()
        self._build_stat_cards()
        self._build_charts()
        self._build_recent_activity()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=28, pady=(24, 20))
        header.grid_columnconfigure(0, weight=1)

        title_block = ctk.CTkFrame(header, fg_color="transparent")
        title_block.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            title_block,
            text="OVERVIEW  /  INVESTIGATIONS",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=PURPLE2,
        ).pack(anchor="w", pady=(0, 5))
        ctk.CTkLabel(
            title_block,
            text="Investigation dashboard",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=TEXT_MAIN,
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_block,
            text="A clear view of current cases, evidence, and investigation priorities.",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_DIM,
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkButton(
            header,
            text="↻   Refresh",
            width=112,
            height=36,
            corner_radius=9,
            fg_color="#ffffff",
            hover_color="#eef1f8",
            border_width=1,
            border_color=SEP_COLOR,
            text_color=TEXT_MAIN,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._refresh,
        ).grid(row=0, column=1, sticky="e")

    def _refresh(self):
        for child in self.winfo_children():
            child.destroy()
        self._build()

    def _build_stat_cards(self):
        stats = get_stat_counts()
        cards_data = [
            ("TOTAL CASES", stats["total_cases"], PURPLE, "CASE"),
            ("ACTIVE CASES", stats["active_cases"], GREEN, "LIVE"),
            ("CRITICAL CASES", stats["critical_cases"], RED, "HIGH"),
            ("EVIDENCE ITEMS", stats["total_evidence"], BLUE, "ITEM"),
            ("TAMPERED ITEMS", stats["tampered"], ORANGE, "ALERT"),
        ]

        cards_row = ctk.CTkFrame(self, fg_color="transparent")
        cards_row.pack(fill="x", padx=22, pady=(0, 18))
        for column in range(len(cards_data)):
            cards_row.grid_columnconfigure(column, weight=1, uniform="stats")

        for column, (label, value, color, tag) in enumerate(cards_data):
            card = ctk.CTkFrame(
                cards_row,
                fg_color=BG_CARD,
                border_color=SEP_COLOR,
                border_width=1,
                corner_radius=14,
            )
            card.grid(row=0, column=column, padx=6, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=15, pady=(14, 8))
            ctk.CTkLabel(
                top,
                text=label,
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color=TEXT_DIM,
            ).pack(side="left")
            ctk.CTkLabel(
                top,
                text=tag,
                font=ctk.CTkFont(size=8, weight="bold"),
                text_color=color,
                fg_color=BG_CARD_ALT,
                corner_radius=5,
            ).pack(side="right", padx=2, pady=1)
            ctk.CTkLabel(
                card,
                text=str(value),
                font=ctk.CTkFont(size=30, weight="bold"),
                text_color=TEXT_MAIN,
            ).pack(anchor="w", padx=15, pady=(0, 14))
            ctk.CTkFrame(card, fg_color=color, height=3, corner_radius=2).pack(
                fill="x", padx=15, pady=(0, 13)
            )

    def _build_charts(self):
        charts_row = ctk.CTkFrame(self, fg_color="transparent")
        charts_row.pack(fill="x", padx=28, pady=(0, 18))
        charts_row.grid_columnconfigure((0, 1), weight=1, uniform="charts")

        bar_card = self._create_panel(charts_row, "Cases by Type", 0)
        type_data = get_cases_by_type()
        if type_data:
            labels = [str(row["case_type"]).replace("_", " ").title() for row in type_data]
            values = [row["total"] for row in type_data]
            colors = [PURPLE, PURPLE2, "#a855f7", BLUE, "#059669",
                      ORANGE, RED, "#ca8a04", "#0d9488"]
            figure, axis = plt.subplots(figsize=(5.4, 2.8), facecolor=BG_CARD)
            axis.set_facecolor(BG_CARD)
            bars = axis.bar(labels, values, color=colors[:len(labels)], width=0.58, zorder=3)
            axis.set_ylabel("Cases", fontsize=9, labelpad=10, color=TEXT_DIM)
            axis.grid(axis="y", zorder=0, linewidth=0.7, color=SEP_COLOR)
            axis.set_axisbelow(True)
            axis.tick_params(axis="x", labelsize=8, rotation=15, length=0, pad=7, colors=TEXT_DIM)
            axis.tick_params(axis="y", labelsize=8, length=0, colors=TEXT_DIM)
            for spine in axis.spines.values():
                spine.set_visible(False)
            axis.set_ylim(0, max(values, default=1) * 1.2)
            for bar, value in zip(bars, values):
                axis.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(values, default=1) * 0.025,
                    str(value),
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    color=TEXT_MAIN,
                )
            figure.tight_layout()
            self._add_chart(bar_card, figure)
        else:
            self._show_empty(bar_card, "No case data available yet.")

        status_card = self._create_panel(charts_row, "Cases by Status", 1)
        status_data = get_cases_by_status()
        if status_data:
            labels = [str(row["status"]).replace("_", " ").title() for row in status_data]
            values = [row["total"] for row in status_data]
            colors = [PURPLE, PURPLE2, "#a855f7", "#db2777", "#0d9488"]
            figure, axis = plt.subplots(figsize=(5.4, 2.8), facecolor=BG_CARD)
            axis.set_facecolor(BG_CARD)
            wedges, _, percentages = axis.pie(
                values,
                labels=None,
                colors=colors[:len(labels)],
                autopct="%1.0f%%",
                pctdistance=0.76,
                wedgeprops={"width": 0.5, "edgecolor": BG_CARD, "linewidth": 2},
                startangle=90,
            )
            for percentage in percentages:
                percentage.set_color("#ffffff")
                percentage.set_fontsize(8)
                percentage.set_fontweight("bold")
            axis.legend(
                wedges,
                labels,
                loc="lower center",
                fontsize=8,
                ncol=min(3, len(labels)),
                frameon=False,
                labelcolor=TEXT_DIM,
                bbox_to_anchor=(0.5, -0.12),
            )
            figure.tight_layout()
            self._add_chart(status_card, figure)
        else:
            self._show_empty(status_card, "No case data available yet.")

    def _create_panel(self, parent, title, column):
        panel = ctk.CTkFrame(
            parent,
            fg_color=BG_CARD,
            border_color=SEP_COLOR,
            border_width=1,
            corner_radius=14,
        )
        panel.grid(
            row=0,
            column=column,
            padx=(0, 8) if column == 0 else (8, 0),
            sticky="nsew",
        )
        ctk.CTkLabel(
            panel,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_MAIN,
        ).pack(anchor="w", padx=18, pady=(15, 2))
        ctk.CTkLabel(
            panel,
            text="Distribution across recorded investigations",
            font=ctk.CTkFont(size=10),
            text_color=TEXT_FAINT,
        ).pack(anchor="w", padx=18, pady=(0, 5))
        return panel

    @staticmethod
    def _add_chart(panel, figure):
        FigureCanvasTkAgg(figure, master=panel).get_tk_widget().pack(
            padx=12, pady=(0, 12), fill="both", expand=True
        )
        plt.close(figure)

    @staticmethod
    def _show_empty(panel, message):
        ctk.CTkLabel(
            panel,
            text=message,
            font=ctk.CTkFont(size=11),
            text_color=TEXT_FAINT,
            height=190,
        ).pack(fill="x", padx=12, pady=(0, 10))

    def _build_recent_activity(self):
        recent_row = ctk.CTkFrame(self, fg_color="transparent")
        recent_row.pack(fill="x", padx=28, pady=(0, 28))
        recent_row.grid_columnconfigure((0, 1), weight=1, uniform="recent")

        cases_card = self._create_panel(recent_row, "Recent Cases", 0)
        recent_cases = get_recent_cases()
        if recent_cases:
            for row in recent_cases:
                priority_colors = {
                    "critical": RED,
                    "high": ORANGE,
                    "medium": "#ca8a04",
                    "low": GREEN,
                }
                color = priority_colors.get(row["priority"], TEXT_DIM)
                item = ctk.CTkFrame(cases_card, fg_color=BG_CARD_ALT, corner_radius=9)
                item.pack(fill="x", padx=13, pady=4)
                top = ctk.CTkFrame(item, fg_color="transparent")
                top.pack(fill="x", padx=12, pady=(9, 3))
                ctk.CTkLabel(
                    top,
                    text=row["case_number"],
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=TEXT_MAIN,
                ).pack(side="left")
                ctk.CTkLabel(
                    top,
                    text=str(row["priority"]).upper(),
                    font=ctk.CTkFont(size=8, weight="bold"),
                    text_color=color,
                ).pack(side="right")
                ctk.CTkLabel(
                    item,
                    text=row["title"],
                    font=ctk.CTkFont(size=10),
                    text_color=TEXT_DIM,
                    wraplength=320,
                    justify="left",
                ).pack(anchor="w", padx=12, pady=(0, 9))
        else:
            self._show_empty(cases_card, "No cases have been recorded.")

        evidence_card = self._create_panel(recent_row, "Recent Evidence", 1)
        recent_evidence = get_recent_evidence()
        if recent_evidence:
            status_colors = {
                "collected": BLUE,
                "in_analysis": ORANGE,
                "verified": GREEN,
                "compromised": RED,
                "released": TEXT_DIM,
            }
            for row in recent_evidence:
                color = status_colors.get(row["status"], TEXT_DIM)
                item = ctk.CTkFrame(evidence_card, fg_color=BG_CARD_ALT, corner_radius=9)
                item.pack(fill="x", padx=13, pady=4)
                top = ctk.CTkFrame(item, fg_color="transparent")
                top.pack(fill="x", padx=12, pady=(9, 3))
                ctk.CTkLabel(
                    top,
                    text=row["evidence_number"],
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=TEXT_MAIN,
                ).pack(side="left")
                ctk.CTkLabel(
                    top,
                    text=str(row["status"]).replace("_", " ").upper(),
                    font=ctk.CTkFont(size=8, weight="bold"),
                    text_color=color,
                ).pack(side="right")
                ctk.CTkLabel(
                    item,
                    text=f"{row['evidence_type'].replace('_', ' ').title()}  ·  {row['case_number']}",
                    font=ctk.CTkFont(size=10),
                    text_color=TEXT_DIM,
                ).pack(anchor="w", padx=12, pady=(0, 9))
        else:
            self._show_empty(evidence_card, "No evidence has been submitted.")
