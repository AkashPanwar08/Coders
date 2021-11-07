
  fetch('https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=5a27d18059f749098ccbc7d4d3611f4f')
  .then((response) => {
    return response.json();
  })
  .then((response) => {
    var data = response.articles;
    var str = ""
    for(let i = 0; i < 3; i++) {
      str+=
      `
      <div class="col-lg-4 py-3 wow fadeInUp">
        <div class="card-blog">
          <div class="header">
            <div class="post-thumb">
              <img src=` + data[i].urlToImage +` alt="" id="image">
            </div>
          </div>
          <div class="body">
            <h5 class="post-title">` + data[i].title + `</h5>
            <div class="post-date">Posted on <a href="#">` + data[i].publishedAt.slice(0, 10) + `</a></div>
          </div>
        </div>
      </div>
      `
    }
  str += `
  <div class="col-12 mt-4 text-center wow fadeInUp">
    <a href="news" class="btn btn-primary">View More</a>
  </div>`
  document.getElementById("data").innerHTML = str;
  })
  .catch((err)=>{
    console.log(err);
  });
