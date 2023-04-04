// const kek = document.querySelector(".kek");
// kek.addEventListener("submit", (e) => {
//   e.preventDefault();
//   fetch("/xyu", { method: "GET" })
//     .then((res) => res.json())
//     .then((data) => console.log(data));
//   console.log("aaxaxaxaxxa");
// });



// ui
const showSearchForm = document.querySelector(".btn_show_form_search");
const searchForm = document.querySelector(".form_search");

showSearchForm.addEventListener("click", () => {
  searchForm.classList.toggle("form_search_shown");
  showSearchForm.classList.toggle("btn_show_rotated")
});
