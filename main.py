import os
from flask import Flask, request, jsonify, send_from_directory
import fitz  # PyMuPDF
import google.generativeai as genai  
from fpdf import FPDF
from werkzeug.utils import secure_filename
import uuid
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
GENERATED_PDF_FOLDER = 'generated_pdfs'

try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")
    model = None

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_PDF_FOLDER, exist_ok=True)


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resumo do Documento', 0, 1, 'C')


def generate_summary_pdf(summary_text: str, output_path: str):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, summary_text)
    pdf.output(output_path)


@app.route('/summarize', methods=['POST'])
def summarize_pdf():
    if not model:
        return jsonify({"error": "A API do Gemini não foi configurada corretamente. Verifique a chave de API."}), 500

    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Arquivo inválido ou não é um PDF"}), 400

    original_filename = secure_filename(file.filename)

    try:
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        num_pages = len(pdf_document)
        full_text = "".join(page.get_text() for page in pdf_document)
        pdf_document.close()

        if not full_text.strip():
            return jsonify({"error": "O PDF não contém texto extraível."}), 400

        prompt = f"""
        Você é um assistente especialista em análise e resumo de documentos. Sua tarefa é ler o texto extraído de um PDF e criar um resumo executivo.

        O resumo deve:
        1. Ser claro, conciso e objetivo.
        2. Capturar as ideias principais e as conclusões do documento.
        3. Ser formatado em parágrafos bem escritos.
        4. Ignorar textos irrelevantes como cabeçalhos, rodapés ou números de página.

        A seguir, o texto do documento:
        ---
        {full_text}
        """

        response = model.generate_content(prompt)

        if not response.parts:
            feedback = response.prompt_feedback
            block_reason = feedback.block_reason.name if feedback.block_reason else "Não especificado"
            return jsonify({"error": f"A resposta foi bloqueada pela API do Gemini. Motivo: {block_reason}"}), 503

        summary = response.text

        unique_id = str(uuid.uuid4())
        summary_pdf_filename = f"resumo_{unique_id}.pdf"
        summary_pdf_path = os.path.join(GENERATED_PDF_FOLDER, summary_pdf_filename)
        generate_summary_pdf(summary, summary_pdf_path)

        download_url = request.host_url.rstrip('/') + f"/download/{summary_pdf_filename}"

        return jsonify({
            "original_filename": original_filename,
            "page_count": num_pages,
            "summary_text": summary,
            "summary_pdf_url": download_url
        })

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro: {str(e)}"}), 500


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(GENERATED_PDF_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5006)