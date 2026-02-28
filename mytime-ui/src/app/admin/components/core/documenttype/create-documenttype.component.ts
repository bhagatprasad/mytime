import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-create-documenttype',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './create-documenttype.component.html',
  styleUrl: './create-documenttype.component.css',
})
export class CreateDocumenttypeComponent {}
