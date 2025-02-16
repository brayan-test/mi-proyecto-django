document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".eliminar-participante").forEach(button => {
        button.addEventListener("click", function() {
            let participanteId = this.getAttribute("data-id");
            let confirmacion = confirm("¿Estás seguro de que deseas eliminar este participante?");
            
            if (confirmacion) {
                fetch(`/participantes/${participanteId}/eliminar/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({})  // Importante para evitar error 400
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Participante eliminado correctamente.");
                        location.reload();
                    } else {
                        alert("Error al eliminar el participante.");
                    }
                })
                .catch(error => console.error("Error:", error));
            }
        });
    });
});

// Función para obtener el CSRF Token de Django
function getCSRFToken() {
    let csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]");
    if (!csrfToken) {
        console.warn("CSRF token no encontrado en la página.");
        return "";
    }
    return csrfToken.value;
}
