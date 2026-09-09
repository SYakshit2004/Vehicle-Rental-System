const githubUsername = "SYakshit2004";
const repository = "Vehicle-Rental-System";
const branch = "main";
const fileName = "Mini Project.py";

const encodedFileName = encodeURIComponent(fileName);

const rawURL =
    `https://raw.githubusercontent.com/${githubUsername}/${repository}/${branch}/${encodedFileName}`;

const githubURL =
    `https://github.com/${githubUsername}/${repository}/blob/${branch}/${encodedFileName}`;

const codeBox = document.getElementById("pythonCode");
const status = document.getElementById("status");
const githubButton = document.getElementById("githubButton");

githubButton.href = githubURL;

fetch(rawURL)
    .then(response => {
        if (!response.ok) {
            throw new Error("Python file could not be loaded");
        }
        return response.text();
    })
    .then(code => {
        codeBox.textContent = code;
        status.textContent = "Loaded";
    })
    .catch(error => {
        console.error(error);
        codeBox.textContent =
`Unable to load the Python source code.

Please check:
1. GitHub username
2. Repository name
3. Branch name
4. Python file name
5. Whether the repository is public

Expected file:
Mini Project.py`;
        status.textContent = "Error";
    });

function copyCode() {
    const code = codeBox.textContent;

    if (!code || code.startsWith("Unable to load")) {
        alert("Python code is not loaded yet.");
        return;
    }

    navigator.clipboard.writeText(code)
        .then(() => {
            const button = document.querySelector(".copy");
            button.textContent = "Copied!";
            setTimeout(() => {
                button.textContent = "Copy Code";
            }, 2000);
        })
        .catch(() => {
            alert("Unable to copy the code.");
        });
}
