import { Injectable } from '@angular/core';
import { ApiService } from '../../common/services/api.service';
import { Observable } from 'rxjs';
import { environment } from '../../../environment';
import { Project } from '../models/project';

@Injectable({ providedIn: 'root' })
export class ProjectService {
  constructor(private apiService: ApiService) { }

  getProjectListAsync(): Observable<Project[]> {
    return this.apiService.send<Project[]>(
      'GET',
      environment.UrlConstants.Project.GetProjectListAsync,
    );
  }

  getProjectListsAsync(): Observable<any> {
    return this.apiService.send<any>(
      'GET',
      environment.UrlConstants.Project.GetProjectListAsync,
    );
  }


  saveProjectAsync(project: Project): Observable<any> {
    return this.apiService.send<any>(
      'POST',
      environment.UrlConstants.Project.InsertOrUpdateProjectAsync,
      project,
    );
  }

  deleteProjectAsync(projectId: number): Observable<any> {
    return this.apiService.send<any>(
      'DELETE',
      `${environment.UrlConstants.Project.DeleteProjectAsync}/${projectId}`,
    );
  }
}
