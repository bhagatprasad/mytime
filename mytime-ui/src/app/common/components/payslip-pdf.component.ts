import { Component, ElementRef, Input, Output, EventEmitter, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { PayslipVM } from '../models/payslip';
import { LoaderService } from '../services/loader.service';

@Component({
  selector: 'app-payslip-pdf',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './payslip-pdf.component.html',
  styleUrls: ['./payslip-pdf.component.css']
})
export class PayslipPdfComponent implements AfterViewInit {

  @ViewChild('payslipContent') payslipContent!: ElementRef;
  @Input() payslipData: PayslipVM | null = null;
  @Input() mode: 'download' | 'preview' = 'download';
  @Output() onPdfGenerated = new EventEmitter<void>();
  @Output() onPdfBlobReady = new EventEmitter<string>();

  officeEmail: string = 'hr@betalen.in';
  logoUrl: string = 'assets/images/logo.png';

  constructor(private loader: LoaderService) {}

  ngAfterViewInit(): void {
    if (!this.payslipData) return;
    setTimeout(() => {
      if (this.mode === 'download') {
        this.generatePDF();
      } else {
        this.generatePreview();
      }
    }, 500);
  }

  formatDate(date: Date | string | null | undefined): string {
    const d = date ? new Date(date) : new Date();
    const day = String(d.getDate()).padStart(2, '0');
    const month = d.toLocaleDateString('en-US', { month: 'long' });
    const year = d.getFullYear();
    return `${day}-${month}-${year}`;
  }

  private async captureCanvas(): Promise<HTMLCanvasElement> {
    const content: HTMLElement = this.payslipContent.nativeElement;
    
    content.style.position = 'fixed';
    content.style.top = '0';
    content.style.left = '0';
    content.style.opacity = '1';
    content.style.visibility = 'visible';
    content.style.width = '800px';
    content.style.height = 'auto';
    content.style.zIndex = '9999';
    content.style.pointerEvents = 'none';
    content.style.backgroundColor = '#ffffff';

    await new Promise(resolve => setTimeout(resolve, 300));

    const canvas = await html2canvas(content, {
      scale: 2,
      logging: false,
      useCORS: true,
      allowTaint: false,
      backgroundColor: '#ffffff',
      width: 800,
      height: content.offsetHeight,
      windowWidth: 800,
      windowHeight: content.offsetHeight,
      onclone: (clonedDoc, element) => {
        const clonedElement = element as HTMLElement;
        clonedElement.style.position = 'fixed';
        clonedElement.style.top = '0';
        clonedElement.style.left = '0';
        clonedElement.style.opacity = '1';
        clonedElement.style.visibility = 'visible';
        clonedElement.style.width = '800px';
        clonedElement.style.height = 'auto';
      }
    });

    content.style.position = 'fixed';
    content.style.top = '-99999px';
    content.style.left = '-99999px';
    content.style.opacity = '0';
    content.style.visibility = 'hidden';
    content.style.zIndex = '-1';

    return canvas;
  }

  async generatePDF(): Promise<void> {
    if (!this.payslipContent || !this.payslipData) { 
      this.loader.hide(); 
      return; 
    }
    
    this.loader.show();
    
    try {
      const canvas = await this.captureCanvas();

      if (!canvas || canvas.width === 0 || canvas.height === 0) {
        console.error('Canvas capture failed - invalid dimensions', canvas?.width, canvas?.height);
        this.loader.hide();
        return;
      }

      const imgData = canvas.toDataURL('image/jpeg', 0.98);
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      });

      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      
      const imgWidth = pageWidth;
      const imgHeight = (canvas.height * pageWidth) / canvas.width;

      pdf.addImage(imgData, 'JPEG', 0, 0, imgWidth, imgHeight);
      
      const fileName = `${this.payslipData?.employee?.EmployeeCode || 'payslip'}-${new Date().getTime()}.pdf`;
      pdf.save(fileName);

    } catch (error) {
      console.error('Error generating PDF:', error);
    } finally {
      this.loader.hide();
      this.onPdfGenerated.emit();
    }
  }

  async generatePreview(): Promise<void> {
    if (!this.payslipContent || !this.payslipData) return;
    
    try {
      const canvas = await this.captureCanvas();

      if (!canvas || canvas.width === 0 || canvas.height === 0) {
        console.error('Preview capture failed - invalid dimensions', canvas?.width, canvas?.height);
        return;
      }

      const imgData = canvas.toDataURL('image/jpeg', 0.98);
      this.onPdfBlobReady.emit(imgData);
    } catch (error) {
      console.error('Error generating preview:', error);
    }
  }
}