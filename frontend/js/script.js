document.addEventListener("DOMContentLoaded", async function () {
    const userData = {
        id: 123456789,
        first_name: "Иван",
        username: "ivan_hero"
    };

    async function loadCharacter() {
        try {
            let response = await fetch("http://127.0.0.1:8000/get_character", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: userData.id })
            });

            let result = await response.json();
            console.log("Данные персонажа:", result);

            if (result.status === "success" && result.character) {
                document.getElementById("username").innerText = userData.username;
                document.getElementById("character-name").innerText = result.character.name ?? "Без имени";
                document.getElementById("level").innerText = result.character.level ?? 1;
                document.getElementById("progress").innerText = `${result.character.progress ?? 0}%`;
                document.getElementById("gold").innerText = result.character.gold ?? 0;
                document.getElementById("crypto").innerText = result.character.crypto ?? 0;
            } else {
                console.warn("Персонаж не найден. Регистрируем нового...");
                await registerUser();
            }
        } catch (error) {
            console.error("Ошибка при загрузке данных персонажа:", error);
        }
    }

    async function registerUser() {
        try {
            let response = await fetch("http://127.0.0.1:8000/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData)
            });

            let result = await response.json();
            console.log("Ответ сервера (регистрация):", result);

            if (result.status === "new_user") {
                console.log("Новый пользователь зарегистрирован, загружаем данные...");
                await loadCharacter();
            }
        } catch (error) {
            console.error("Ошибка при регистрации пользователя:", error);
        }
    }

    // Загружаем персонажа, если его нет — регистрируем
    await loadCharacter();
});
