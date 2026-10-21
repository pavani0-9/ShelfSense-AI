# 🛒 ShelfSense AI — Smart Bazaar Finder

## 🌐 Live Demo : https://shelfsense-ai-09.streamlit.app/
**An AI-powered smart product catalogue for discovering products, exploring categories, and finding products more easily.**

## 📌 About the Project

ShelfSense AI is a web application built with Python and Streamlit that helps users browse a retail product catalogue through a simple and user-friendly interface.

The application organizes products into categories and displays product information, including names, prices, and images where available. It aims to make product discovery easier and provide a convenient digital shopping experience.

## ✨ Features

- 🛍️ **Product Catalogue:** Browse products from the retail dataset.
- 🗂️ **Product Categories:** Explore available product categories.
- 🖼️ **Product Images:** Display product images using the associated image files.
- 💰 **Product Pricing:** View product prices in the catalogue.
- 🔎 **Product Discovery:** Find and explore products through the app's available browsing and filtering options.
- 📱 **Interactive Interface:** Navigate the application using Streamlit.
- ☁️ **Online Deployment:** Access the application through its deployed Streamlit website.

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Interactive web interface |
| Pandas | Dataset loading and processing |
| Git and GitHub | Version control and source code hosting |
| Streamlit Community Cloud | Web application deployment |

## 📂 Project Structure

```text
ShelfSense-AI/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── data/
│   ├── retail_products.csv # Retail product dataset
│   └── products.csv        # Additional product data, if used
│
└── product_images/
    └── train/              # Product images used by the application
```

*Note: The exact files and folders may vary depending on the version of the project in your repository.*

## 📊 Dataset

ShelfSense AI uses a retail product dataset containing product information and image identifiers.

The dataset is used to load and organize product details for display in the application.

The product image files are stored separately in the `product_images/train/` directory. The application associates the relevant images with products using their image identifiers.

**Important:** The dataset CSV files and image files must be available at the expected paths for the product catalogue and images to load correctly.

## ⚙️ Installation and Setup

### 1. Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/pavani0-9/ShelfSense-AI.git
```

### 2. Open the project directory

```bash
cd ShelfSense-AI
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser. If it does not open automatically, use the local URL displayed in your terminal, usually:

`http://localhost:8501`

## ☁️ Deployment

The application can be deployed using Streamlit Community Cloud.

1. Push the project files to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub account.
4. Select the `ShelfSense-AI` repository.
5. Select the `main` branch.
6. Set `app.py` as the main application file.
7. Deploy the application.

### Deployment Requirements

- Include `app.py` and `requirements.txt` in the repository.
- Ensure the required dataset files are accessible to the deployed application.
- Ensure product image paths point to files included in the repository or to a publicly accessible image source.
- Keep file and folder names consistent with those used in the application code.

## 🖼️ Product Images

Product images are stored in the `product_images/train/` directory.

For the images to appear on the deployed website:

- The image files must be committed and pushed to GitHub.
- The deployed application must use the correct relative or application-based paths.
- The image filenames must match the image identifiers used by the dataset.
- The application must handle missing images gracefully.

## 🚀 Future Enhancements

- AI-based product recommendations.
- Smart product search.
- Product comparisons.
- Personalized shopping suggestions.
- Improved product filtering and sorting.
- Enhanced product availability and aisle information.

## 👩‍💻 Author

**Pavani**

GitHub: [@pavani0-9](https://github.com/pavani0-9)

## 📄 License

This project is intended for educational and development purposes. Please check the original dataset's license and usage terms before redistributing its data or images. Add a project license if you intend to publish the code under specific reuse terms.

---

⭐ **If you find ShelfSense AI interesting, feel free to explore the repository and follow its development!**
