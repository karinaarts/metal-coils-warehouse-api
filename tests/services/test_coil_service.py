import pytest
from fastapi import HTTPException

from src.schemas.coil_schema import CoilAddSchema, CoilFilterSchema


@pytest.mark.asyncio
async def test_create_coil(
    coil_service, mock_session, sample_coil_data, sample_coil_model
):
    coil_service.repository.add.return_value = sample_coil_model
    schema = CoilAddSchema(**sample_coil_data)

    result = await coil_service.create(mock_session, schema)

    coil_service.repository.add.assert_called_once_with(
        mock_session, sample_coil_data
    )
    assert result.id == sample_coil_model.id
    assert result.length == sample_coil_model.length
    assert result.weight == sample_coil_model.weight
    assert result.creation_date == sample_coil_model.creation_date
    assert result.deletion_date is None


@pytest.mark.asyncio
async def test_delete_coil(coil_service, mock_session, deleted_coil_model):
    coil_service.repository.delete.return_value = deleted_coil_model

    result = await coil_service.delete(mock_session, deleted_coil_model.id)

    coil_service.repository.delete.assert_called_once_with(
        mock_session, deleted_coil_model.id
    )
    assert result.id == deleted_coil_model.id
    assert result.deletion_date is not None


@pytest.mark.asyncio
async def test_get_all_coils(
    coil_service, mock_session, sample_coil_model, deleted_coil_model
):
    coil_service.repository.get_all.return_value = [
        sample_coil_model,
        deleted_coil_model,
    ]

    result = await coil_service.get_all(mock_session)

    coil_service.repository.get_all.assert_called_once_with(mock_session)
    assert len(result) == 2
    assert result[0].id == sample_coil_model.id
    assert result[1].id == deleted_coil_model.id


@pytest.mark.asyncio
async def test_get_filtered_coils(
    coil_service, mock_session, sample_coil_model
):
    filter_data = {"length_min": 50.0, "weight_max": 600.0}
    filter_schema = CoilFilterSchema(**filter_data)
    coil_service.repository.get_filtered.return_value = [sample_coil_model]

    result = await coil_service.get_filtered(mock_session, filter_schema)

    coil_service.repository.get_filtered.assert_called_once()
    assert len(result) == 1
    assert result[0].id == sample_coil_model.id


@pytest.mark.asyncio
async def test_delete_nonexistent_coil(coil_service, mock_session):
    coil_service.repository.delete.side_effect = HTTPException(
        status_code=404, detail="Coil is not found"
    )

    with pytest.raises(HTTPException) as exc_info:
        await coil_service.delete(mock_session, 999)

    assert exc_info.value.status_code == 404
    assert "not found" in exc_info.value.detail


@pytest.mark.asyncio
async def test_delete_already_deleted_coil(coil_service, mock_session):
    coil_service.repository.delete.side_effect = HTTPException(
        status_code=400, detail="Coil already deleted"
    )

    with pytest.raises(HTTPException) as exc_info:
        await coil_service.delete(mock_session, 1)

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_get_filtered_coils_empty_result(coil_service, mock_session):
    filter_data = {"length_min": 1000.0, "weight_max": 2000.0}
    filter_schema = CoilFilterSchema(**filter_data)
    coil_service.repository.get_filtered.return_value = []

    result = await coil_service.get_filtered(mock_session, filter_schema)

    assert len(result) == 0
