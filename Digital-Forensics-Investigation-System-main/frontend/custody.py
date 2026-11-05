import customtkinter as ctk
from backend.custody_service import get_all_evidence_numbers, get_custody_trail, get_integrity_records

BG_DARK   = "#f3f5fa"
BG_CARD   = "#ffffff"
BG_CARD_ALT= "#f5f7fc"
PURPLE    = "#4f46e5"
PURPLE2   = "#6d5ce8"
TEXT_MAIN = "#172033"
TEXT_DIM  = "#596579"
TEXT_FAINT= "#8290a5"
GREEN     = "#15803d"
RED       = "#dc3545"
ORANGE    = "#d97706"
BLUE      = "#2563eb"


class CustodyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, session, mode="custody", **kwargs):
        super().__init__(master, **kwargs)
        self.session = session
        self.mode    = mode
        self.configure(fg_color=BG_DARK, scrollbar_button_color="#d5dce8")
        self._build()

    def _build(self):
        if self.mode == "integrity":
            self._build_integrity()
        else:
            self._build_custody()

    def _build_custody(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=28, pady=(22, 0))
        ctk.CTkLabel(hdr, text="Chain of Custody Tracker",
                     font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Full audit trail — who handled what, when, and where",
                     font=ctk.CTkFont(size=12), text_color=TEXT_DIM).pack(anchor="w")
        ctk.CTkFrame(self, fg_color="#e4e9f2", height=1).pack(fill="x", padx=28, pady=14)

        ev_list = get_all_evidence_numbers()
        ctk.CTkLabel(self, text="SELECT EVIDENCE ITEM",
                     font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXT_DIM).pack(padx=28, anchor="w")
        self.ev_var = ctk.StringVar(value=ev_list[0] if ev_list else "")
        ctk.CTkOptionMenu(self, values=ev_list, variable=self.ev_var,
                          fg_color=BG_CARD, button_color=PURPLE, button_hover_color=PURPLE2,
                          text_color=TEXT_MAIN, height=40,
                          command=lambda _: self._load_custody()).pack(fill="x", padx=28, pady=(4, 14))

        self.custody_container = ctk.CTkFrame(self, fg_color="transparent")
        self.custody_container.pack(fill="x", padx=28, pady=(0, 28))
        if ev_list:
            self._load_custody()

    def _load_custody(self):
        for w in self.custody_container.winfo_children():
            w.destroy()

        rows = get_custody_trail(self.ev_var.get())
        if not rows:
            ctk.CTkLabel(self.custody_container,
                         text="No custody records found for this evidence item.",
                         font=ctk.CTkFont(size=13), text_color=ORANGE).pack(pady=20)
            return

        summary = ctk.CTkFrame(self.custody_container, fg_color="#eaf7ef",
                                border_color="#bbdfc8", border_width=1, corner_radius=10)
        summary.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(summary, text=f"{len(rows)} custody record(s) found for {self.ev_var.get()}",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=GREEN).pack(padx=16, pady=10)

        action_icons = {
            "collected": "Collected", "transferred": "Transferred", "analyzed": "Analyzed",
            "stored": "Stored", "returned": "Returned", "destroyed": "Destroyed",
            "released_to_court": "Released to Court"
        }

        for i, row in enumerate(rows):
            card = ctk.CTkFrame(self.custody_container, fg_color=BG_CARD,
                                 border_color="#e4e9f2", border_width=1, corner_radius=12)
            card.pack(fill="x", pady=4)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=18, pady=14)

            top = ctk.CTkFrame(inner, fg_color="transparent")
            top.pack(fill="x")
            ctk.CTkLabel(top, text=f"  Step {i+1}  ",
                         font=ctk.CTkFont(size=9, weight="bold"),
                         fg_color="#eef0ff", text_color=PURPLE, corner_radius=8).pack(side="left")
            ctk.CTkLabel(top, text=f"  {action_icons.get(row['action_type'], row['action_type']).upper()}",
                         font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT_MAIN).pack(side="left", padx=10)
            ctk.CTkLabel(top, text=str(row["action_time"]),
                         font=ctk.CTkFont(size=10), text_color="#64748b").pack(side="right")

            details = ctk.CTkFrame(inner, fg_color="transparent")
            details.pack(fill="x", pady=(10, 0))
            details.columnconfigure((0, 1), weight=1)
            self._detail_item(details, "Handled By", row["handled_by"], 0, 0)
            self._detail_item(details, "Location",   row["location"] or "—", 1, 0)
            self._detail_item(details, "Reason",     row["reason"] or "—",   0, 1)
            self._detail_item(details, "Witness",    row["witness_name"] or "None", 1, 1)

    def _detail_item(self, parent, label, value, row, col):
        frame = ctk.CTkFrame(parent, fg_color=BG_CARD_ALT,
                              border_color="#e4e9f2", border_width=1, corner_radius=8)
        frame.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=TEXT_DIM).pack(padx=10, pady=(8, 2), anchor="w")
        ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=12),
                     text_color=TEXT_MAIN, wraplength=250, justify="left").pack(padx=10, pady=(0, 8), anchor="w")

    def _build_integrity(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=28, pady=(22, 0))
        ctk.CTkLabel(hdr, text="Evidence Integrity Verification",
                     font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_MAIN).pack(anchor="w")

        info = ctk.CTkFrame(self, fg_color="#eef0ff", border_color="#d9ddfb", border_width=1, corner_radius=10)
        info.pack(fill="x", padx=28, pady=14)
        ctk.CTkLabel(info, text="SHA-256 hash verification — detects tampered evidence",
                     font=ctk.CTkFont(size=12), text_color="#3730a3").pack(padx=16, pady=10)

        rows = get_integrity_records()
        tampered = [r for r in rows if r["is_tampered"]]
        clean    = [r for r in rows if not r["is_tampered"]]

        if tampered:
            alert = ctk.CTkFrame(self, fg_color="#fff0f0", border_color="#f0caca", border_width=1, corner_radius=10)
            alert.pack(fill="x", padx=28, pady=(0, 8))
            ctk.CTkLabel(alert, text=f"{len(tampered)} tampered evidence item(s) detected!",
                         font=ctk.CTkFont(size=13, weight="bold"), text_color=RED).pack(padx=16, pady=10)
            for r in tampered:
                self._integrity_card(r, tampered=True)
            ctk.CTkFrame(self, fg_color="#e4e9f2", height=1).pack(fill="x", padx=28, pady=10)

        clean_banner = ctk.CTkFrame(self, fg_color="#eaf7ef", border_color="#bbdfc8", border_width=1, corner_radius=10)
        clean_banner.pack(fill="x", padx=28, pady=(0, 8))
        ctk.CTkLabel(clean_banner, text=f"{len(clean)} evidence item(s) verified clean",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=GREEN).pack(padx=16, pady=10)
        for r in clean:
            self._integrity_card(r, tampered=False)
        ctk.CTkFrame(self, fg_color="transparent", height=28).pack()

    def _integrity_card(self, row, tampered):
        clr = RED if tampered else GREEN
        card = ctk.CTkFrame(self, fg_color=BG_CARD, border_color=clr, border_width=1, corner_radius=12)
        card.pack(fill="x", padx=28, pady=4)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")
        ctk.CTkLabel(top, text=row["evidence_number"],
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(top, text=f"  {'TAMPERED' if tampered else 'CLEAN'}  ",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     fg_color="#eaf7ef" if not tampered else "#fff0f0",
                     text_color=clr, corner_radius=10).pack(side="left", padx=8)
        ctk.CTkLabel(top, text=row["evidence_type"],
                     font=ctk.CTkFont(size=10), text_color=TEXT_FAINT).pack(side="left")

        ctk.CTkLabel(inner,
                     text=f"Case: {row['case_number']}  |  Verified by: {row['verified_by']}  |  {row['verified_at']}",
                     font=ctk.CTkFont(size=10), text_color=TEXT_DIM).pack(anchor="w", pady=(4, 4))

        hash_frame = ctk.CTkFrame(inner, fg_color=BG_CARD_ALT,
                                   border_color="#e4e9f2", border_width=1, corner_radius=8)
        hash_frame.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(hash_frame, text="SHA-256", font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=TEXT_DIM).pack(padx=12, pady=(6, 2), anchor="w")
        ctk.CTkLabel(hash_frame, text=row["sha256_hash"],
                     font=ctk.CTkFont(family="Courier New", size=10),
                     text_color=BLUE).pack(padx=12, pady=(0, 6), anchor="w")

        if row["notes"]:
            ctk.CTkLabel(inner, text=f"Note: {row['notes']}",
                         font=ctk.CTkFont(size=11), text_color=TEXT_DIM).pack(anchor="w")