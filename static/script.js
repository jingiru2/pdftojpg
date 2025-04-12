// 파일 위치: pdfproject/static/script.js

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('upload-form');
  const fileInput = document.getElementById('pdf-file');
  const resultSection = document.getElementById('result-section');
  const imageList = document.getElementById('image-list');
  const downloadAll = document.getElementById('download-all');

  form.addEventListener('submit', async function (e) {
    e.preventDefault(); // 기본 form 제출 막기

    const file = fileInput.files[0];
    if (!file) {
      alert("PDF 파일을 선택해주세요!");
      return;
    }

    const formData = new FormData();
    formData.append('pdf', file);

    try {
      const response = await fetch('/convert', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error("변환 실패");

      const data = await response.json();

      if (data.success) {
        // 이미지 표시
        imageList.innerHTML = '';
        data.images.forEach(imgUrl => {
          const img = document.createElement('img');
          img.src = imgUrl;
          img.alt = 'Converted JPG';
          imageList.appendChild(img);
        });

        // 전체 다운로드 링크 설정
        downloadAll.href = data.zip_url;
        downloadAll.style.display = 'inline-block';
        resultSection.style.display = 'block';
      } else {
        alert("이미지 변환에 실패했어요 😥");
      }
    } catch (error) {
      console.error(error);
      alert("에러가 발생했어요! 콘솔을 확인해주세요.");
    }
  });
});
