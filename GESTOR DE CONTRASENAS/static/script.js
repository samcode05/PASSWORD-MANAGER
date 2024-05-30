document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('showPasswordsBtn').addEventListener('click', fetchPasswords);
    document.getElementById('addPasswordBtn').addEventListener('click', showAddPasswordForm);
    document.getElementById('formAddPassword').addEventListener('submit', addPassword);
    document.getElementById('editPasswordBtn').addEventListener('click', editPassword);
    document.getElementById('deletePasswordBtn').addEventListener('click', deletePassword);
    document.getElementById('productSelect').addEventListener('change', toggleEditDeleteButtons);

    // Asignar eventos a los botones de importar, exportar y generar contraseñas
    document.getElementById('generatePasswordBtn').addEventListener('click', generateRandomPassword);
    document.getElementById('importPasswordsBtn').addEventListener('click', importPasswords);
    document.getElementById('exportPasswordsBtn').addEventListener('click', exportPasswords);
});

function fetchPasswords() {
    fetch('/ver_productos')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('productSelect');
            select.innerHTML = '';
            data.productos.forEach(producto => {
                const option = document.createElement('option');
                option.value = producto.id;
                option.textContent = producto.nombre;
                select.appendChild(option);
            });
            document.getElementById('passwordList').style.display = 'block';
        });
}

function showAddPasswordForm() {
    document.getElementById('addPasswordForm').style.display = 'block';
}

function addPassword(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;

    fetch('/crear_producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre: name,
            contrasena: password,
            correo: email
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchPasswords();
        document.getElementById('addPasswordForm').style.display = 'none';
        document.getElementById('formAddPassword').reset();
    });
}

function editPassword() {
    const selectedProductId = parseInt(document.getElementById('productSelect').value);
    const name = prompt("Ingrese el nuevo nombre:");
    const password = prompt("Ingrese la nueva contraseña:");
    const email = prompt("Ingrese el nuevo correo:");

    fetch('/editar_producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: selectedProductId,
            nombre: name,
            contrasena: password,
            correo: email
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchPasswords();
    });
}

function deletePassword() {
    const selectedProductId = parseInt(document.getElementById('productSelect').value);

    fetch('/eliminar_producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: selectedProductId })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchPasswords();
    });
}

function toggleEditDeleteButtons() {
    const select = document.getElementById('productSelect');
    const editBtn = document.getElementById('editPasswordBtn');
    const deleteBtn = document.getElementById('deletePasswordBtn');
    if (select.value) {
        editBtn.style.display = 'block';
        deleteBtn.style.display = 'block';
    } else {
        editBtn.style.display = 'none';
        deleteBtn.style.display = 'none';
    }
}

function generateRandomPassword() {
    const length = prompt("Ingrese la longitud de la contraseña (por defecto 12):", 12);
    fetch(`/generar_contrasena_random?length=${length}`)
        .then(response => response.json())
        .then(data => {
            alert(`Contraseña generada: ${data.contrasena}`);
        });
}

function importPasswords() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.csv';
    fileInput.onchange = function(event) {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            
            fetch('/importar_contrasenas', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                fetchPasswords();
            });
        }
    };
    fileInput.click();
}

function exportPasswords() {
    fetch('/exportar_contrasenas')
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error('Error al exportar contraseñas');
            }
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'passwords.csv';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            alert(error.message);
        });
}


