import os
import json
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption, PowerpointFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TesseractCliOcrOptions
)
from docling_core.types.doc import ImageRefMode
from PIL import Image


def example_usage(source_file_path: str):
    # Ensure absolute path
    source_file_path = Path(source_file_path).expanduser().resolve()
    if not source_file_path.exists():
        raise FileNotFoundError(f"File not found: {source_file_path}")

    base_file_name = source_file_path.stem
    output_dir = Path("output")
    images_dir = output_dir / f"{base_file_name}_images"
    output_dir.mkdir(exist_ok=True)
    images_dir.mkdir(exist_ok=True)
    print(f"Output directory: {output_dir}")
    print(f"Images directory: {images_dir}")

    # Configure PDF pipeline options (used only for PDFs)
    pipeline_options = PdfPipelineOptions(generate_picture_images=True)
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    pipeline_options.do_formula_enrichment = True
    ocr_opts = TesseractCliOcrOptions(force_full_page_ocr=True)
    pipeline_options.ocr_options = ocr_opts

    # Detect format
    ext = source_file_path.suffix.lower()
    if ext == ".pdf":
        fmt = InputFormat.PDF
    elif ext == ".pptx":
        fmt = InputFormat.PPTX
    else:
        raise ValueError(f"Unsupported input file type: {ext}")

    # Create converter
    format_opts = {}
    if fmt == InputFormat.PDF:
        format_opts[InputFormat.PDF] = PdfFormatOption(pipeline_options=pipeline_options)
    elif fmt == InputFormat.PPTX:
        format_opts[InputFormat.PPTX] = PowerpointFormatOption()

    converter = DocumentConverter(format_options=format_opts)

    # Convert
    result = converter.convert(str(source_file_path))
    doc = result.document

    # Save extracted images
    for i, picture_item in enumerate(doc.pictures):
        try:
            pil_image = picture_item.get_image(doc)
            image_name = f"image_{i+1}.png"
            image_path = images_dir / image_name
            pil_image.save(image_path)
            print(f"Image saved: {image_path}")
            picture_item.image.filepath = str(images_dir.name / image_name)
        except Exception as e:
            print(f"Could not extract or save an image: {e}")

    # Save Markdown
    markdown_path = output_dir / f"{base_file_name}.md"
    doc.save_as_markdown(markdown_path, image_mode=ImageRefMode.REFERENCED)
    print(f"Markdown file saved: {markdown_path}")

    # Save JSON
    json_path = output_dir / f"{base_file_name}.json"
    try:
        doc.save_as_json(json_path)
    except AttributeError:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(doc.export_to_dict(), f, indent=2)
    print(f"JSON file saved: {json_path}")


if __name__ == "__main__":
    file_path = input("Enter PDF or PPTX file path: ").strip()
    if file_path:
        example_usage(file_path)
    else:
        print("Please provide a file path.")