const searchInput = document.getElementById("searchInput");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        const searchText = this.value.toLowerCase();

        const rows = document.querySelectorAll(
            "#fileTable tbody tr"
        );

        rows.forEach(function (row) {

            const fileName = row
                .querySelector(".file-info strong")
                .textContent
                .toLowerCase();

            if (fileName.includes(searchText)) {

                row.style.display = "";

            } else {

                row.style.display = "none";

            }

        });

    });

}