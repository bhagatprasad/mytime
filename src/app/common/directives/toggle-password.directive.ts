import { Directive, ElementRef, Renderer2 } from '@angular/core';

@Directive({
  selector: '[appTogglePassword]',
  standalone: true
})
export class TogglePasswordDirective {

  private isVisible = false;
  private icon!: HTMLElement;

  constructor(private el: ElementRef<HTMLInputElement>,
              private renderer: Renderer2) {

    this.setParentRelative();
    this.createIcon();
  }

  private setParentRelative() {
    const parent = this.el.nativeElement.parentElement!;
    this.renderer.setStyle(parent, 'position', 'relative');
  }

  private createIcon() {
    this.icon = this.renderer.createElement('i');

    this.renderer.addClass(this.icon, 'mdi');
    this.renderer.addClass(this.icon, 'mdi-eye-outline');
    this.renderer.addClass(this.icon, 'text-muted');

    this.renderer.setStyle(this.icon, 'position', 'absolute');
    this.renderer.setStyle(this.icon, 'right', '15px');
    this.renderer.setStyle(this.icon, 'top', '50%');
    this.renderer.setStyle(this.icon, 'transform', 'translateY(-50%)');
    this.renderer.setStyle(this.icon, 'cursor', 'pointer');
    this.renderer.setStyle(this.icon, 'z-index', '10');

    // 👇 Attach click directly to icon
    this.renderer.listen(this.icon, 'click', () => {
      this.toggle();
    });

    this.renderer.appendChild(
      this.el.nativeElement.parentElement,
      this.icon
    );
  }

  private toggle() {
    this.isVisible = !this.isVisible;

    this.renderer.setAttribute(
      this.el.nativeElement,
      'type',
      this.isVisible ? 'text' : 'password'
    );

    this.renderer.removeClass(this.icon, 'mdi-eye-outline');
    this.renderer.removeClass(this.icon, 'mdi-eye-off-outline');

    this.renderer.addClass(
      this.icon,
      this.isVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'
    );
  }
}
