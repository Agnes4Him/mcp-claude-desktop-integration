from utils.path_bootstrap import ensure_src_on_path
ensure_src_on_path()

from auth.get_docs_service import get_docs_service

def extract_text_from_doc(doc):
    text = []

    for element in doc.get("body", {}).get("content", []):
        paragraph = element.get("paragraph")
        if not paragraph:
            continue

        for elem in paragraph.get("elements", []):
            run = elem.get("textRun")
            if run:
                text.append(run.get("content", ""))

    return "".join(text).strip()


def get_email_style_guide(doc_id: str) -> str:
    service = get_docs_service()
    doc = service.documents().get(documentId=doc_id).execute()
    return extract_text_from_doc(doc)