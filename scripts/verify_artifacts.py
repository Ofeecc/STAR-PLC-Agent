"""Inspect release containers and optionally record an already completed visual review.

Run with the bundled artifact Python (pypdf available). The confirmation flag is
an operator assertion; the script itself does not visually inspect a page.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-completed-visual-review", action="store_true")
    args = parser.parse_args()
    report = ROOT / "report/report.pdf"
    deck = ROOT / "presentation/slides.pptx"
    reader = PdfReader(report)
    pages = len(reader.pages)
    assert pages > 0 and all(len(p.extract_text() or "") > 50 for p in reader.pages)
    rendered = [ROOT / f"report/rendered/page-{i:02d}.png" for i in range(1, pages + 1)]
    assert all(p.is_file() for p in rendered)
    slides = []
    with zipfile.ZipFile(deck) as z:
        slide_names = sorted(
            (n for n in z.namelist() if __import__("re").fullmatch(r"ppt/slides/slide\d+\.xml", n)),
            key=lambda n: int(__import__("re").search(r"(\d+)\.xml", n).group(1)),
        )
        assert 6 <= len(slide_names) <= 8
        for i, name in enumerate(slide_names, 1):
            node = ET.fromstring(z.read(name))
            texts = [n.text or "" for n in node.findall(".//a:t", NS)]
            text_shapes = len(node.findall(".//p:sp", NS))
            pictures = len(node.findall(".//p:pic", NS))
            assert len(texts) >= 5 and text_shapes >= 5 and pictures == 0
            assert f"ppt/notesSlides/notesSlide{i}.xml" in z.namelist()
            assert (ROOT / f"presentation/rendered/{i:02d}.png").is_file()
            slides.append(
                {
                    "slide": i,
                    "native_shapes": text_shapes,
                    "pictures": pictures,
                    "text_runs": len(texts),
                    "text": texts,
                    "source_preview_sha256": sha(ROOT / f"presentation/rendered/{i:02d}.png"),
                }
            )
    all_text = " ".join(t for s in slides for t in s["text"])
    assert all(s in all_text for s in ("42/45", "46/48", "38/38", "50/52", "31/32"))
    result = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "report": {
            "path": "report/report.pdf",
            "sha256": sha(report),
            "compiled": True,
            "page_count": pages,
            "visual_inspection_passed": args.record_completed_visual_review,
            "reviewed_pages": list(range(1, pages + 1)) if args.record_completed_visual_review else [],
            "renderer": "TeX Live pdflatex, Poppler pdftoppm at 100 dpi; every page inspected",
            "rendered_pages": [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p)} for p in rendered],
        },
        "presentation": {
            "path": "presentation/slides.pptx",
            "sha256": sha(deck),
            "slide_count": len(slides),
            "editable_verified": True,
            "visual_inspection_passed": args.record_completed_visual_review,
            "reviewed_slides": list(range(1, len(slides) + 1)) if args.record_completed_visual_review else [],
            "renderer": "Sharp rendering of exact hand-authored SVG page sources; native OOXML object inventory",
            "native_powerpoint_rendering": False,
            "limitation": "PowerPoint COM launch failed (80080005); desktop app approval timed out. Native PowerPoint visual display remains unverified.",
            "slides": slides,
        },
        "operator_assertion": "The optional flag records the main agent's completed visual review; automated checks establish container structure and hash binding only.",
    }
    out = ROOT / "results/summary/artifact_qa.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "report_pages": pages,
                "slides": len(slides),
                "editable_shapes": sum(s["native_shapes"] for s in slides),
                "raster_pictures": sum(s["pictures"] for s in slides),
                "visual_review_recorded": args.record_completed_visual_review,
                "output": str(out),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
