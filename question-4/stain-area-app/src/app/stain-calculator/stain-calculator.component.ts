import { Component } from '@angular/core';

@Component({
  selector: 'app-stain-calculator',
  templateUrl: './stain-calculator.component.html',
  styleUrls: ['./stain-calculator.component.css']
})
export class StainCalculatorComponent {
  imageSrc: string | ArrayBuffer | null = null;
  points: number = 1000;
  area: number | null = null;
  history: { points: number, area: number }[] = [];

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.imageSrc = e.target?.result ?? null;
      };
      reader.readAsDataURL(input.files[0]);
    }
  }

  calculateArea(): void {
    if (!this.imageSrc || typeof this.imageSrc !== 'string') {
      alert('Por favor, carga una imagen primero.');
      return;
    }

    const img = new Image();
    img.src = this.imageSrc;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;

      let insideCount = 0;

      for (let i = 0; i < this.points; i++) {
        const x = Math.floor(Math.random() * canvas.width);
        const y = Math.floor(Math.random() * canvas.height);
        const index = (y * canvas.width + x) * 4;

        if (data[index] > 200) {
          insideCount++;
        }
      }

      const totalPixels = canvas.width * canvas.height;
      const estimatedArea = (insideCount / this.points) * totalPixels;

      this.area = estimatedArea;
      this.history.unshift({ points: this.points, area: estimatedArea });
    };
  }
}
