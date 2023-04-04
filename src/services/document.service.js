import api from './api';

class DocumentService {
	getWaitingDocuments() {
		return api.get('/doc/waiting');
	}

	getDocumentDetail(documentID) {
		return api.get(`/doc/detail/${documentID}`);
	}
}

export default new DocumentService()