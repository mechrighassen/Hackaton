import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlgorithmNewComponent } from './algorithm-new.component';

describe('AlgorithmNewComponent', () => {
  let component: AlgorithmNewComponent;
  let fixture: ComponentFixture<AlgorithmNewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlgorithmNewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlgorithmNewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
