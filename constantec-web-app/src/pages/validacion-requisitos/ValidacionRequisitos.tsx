import { useEffect, useMemo, useState } from 'react'
import { Flex, Text, Button, Separator, Spinner } from '@radix-ui/themes'
import { useGetUsuario } from './useGetUsuario'
import { usePostComprobante } from './usePostComprobante'
import { useGetEstadoComprobante } from './useGetEstadoComprobante'

export const IdEstadoComprobante = {
  SIN_COMPROBANTE: 1,
  PENDIENTE: 2,
  RECHAZADO: 3,
  APROBADO: 4,
} as const

type EstadoValidacion =
  (typeof IdEstadoComprobante)[keyof typeof IdEstadoComprobante]

const MAX_MB = 5
const MAX_BYTES = MAX_MB * 1024 * 1024
const ALLOWED_TYPES = ['application/pdf', 'image/png', 'image/jpeg']

export function ValidacionRequisitos() {
  const { data: estudiante } = useGetUsuario()
  const { mutate, isPending } = usePostComprobante()
  const { data: comprobante } = useGetEstadoComprobante(estudiante?.no_control)

  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)

  const data = useMemo(() => {
    return comprobante || { estado: IdEstadoComprobante.SIN_COMPROBANTE }
  }, [comprobante])

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] ?? null
    setError(null)
    if (!selected) return

    if (!ALLOWED_TYPES.includes(selected.type)) {
      setError('Formato no permitido. Solo PDF, JPG o PNG.')
      return
    }
    if (selected.size > MAX_BYTES) {
      setError(`El archivo excede ${MAX_MB} MB.`)
      return
    }
    setFile(selected)
  }

  const handleEnviar = () => {
    if (!file || !estudiante?.no_control) {
      setError('Información incompleta para el envío.')
      return
    }

    const formData = new FormData()
    formData.append('archivo', file)
    formData.append('no_control', estudiante.no_control)

    mutate(formData, {
      onSuccess: () => {
        setFile(null)
        setError(null)
      },
      onError: (err: any) => {
        setError(err.response?.data?.detail || 'Error al subir el archivo')
      },
    })
  }

  const estadoTexto = useMemo(() => {
    const textos: Record<EstadoValidacion, string> = {
      [IdEstadoComprobante.SIN_COMPROBANTE]: 'Sin comprobante',
      [IdEstadoComprobante.PENDIENTE]: 'Pendiente de validación',
      [IdEstadoComprobante.RECHAZADO]: 'Rechazado',
      [IdEstadoComprobante.APROBADO]: 'Aprobado',
    }
    return textos[data.estado] || 'Desconocido'
  }, [data.estado])

  const puedeSubir =
    data.estado === IdEstadoComprobante.SIN_COMPROBANTE ||
    data.estado === IdEstadoComprobante.RECHAZADO

  return (
    <Flex width="100%" justify="center">
      <Flex
        direction="column"
        style={{ maxWidth: 720, width: '100%' }}
        gap="3"
        p="4"
      >
        <Text size="7" weight="bold" align="center" mt="4">
          Validación de Requisitos
        </Text>

        <Text color="gray" align="center">
          Para continuar con el trámite de tu constancia, sube tu comprobante de
          pago (PDF o imagen). El documento será revisado por el personal
          administrativo.
        </Text>

        <Separator size="4" />

        <Text>
          <strong>Estado: </strong>
          <Text
            color={
              data.estado === IdEstadoComprobante.APROBADO
                ? 'green'
                : data.estado === IdEstadoComprobante.RECHAZADO
                  ? 'red'
                  : 'orange'
            }
            mt="2"
          >
            {estadoTexto}
          </Text>
        </Text>

        {data.archivoNombre && (
          <Text color="gray" size="2">
            Archivo registrado: {data.archivoNombre}
          </Text>
        )}

        {data.estado === IdEstadoComprobante.PENDIENTE && (
          <Text color="gray" size="2">
            Tu comprobante está en revisión. Espera la validación del personal
            administrativo.
          </Text>
        )}

        {data.estado === IdEstadoComprobante.RECHAZADO &&
          data.motivo_rechazo && (
            <Text color="red" weight="bold">
              <strong>Motivo de rechazo:</strong> {data.motivo_rechazo}
            </Text>
          )}

        {data.estado === IdEstadoComprobante.APROBADO && (
          <Text color="green">
            Tu comprobante ha sido aprobado. Puedes continuar con la solicitud.
          </Text>
        )}

        <Separator size="4" />

        {puedeSubir && (
          <Flex direction="column" gap="3">
            <Text weight="bold">Subir comprobante</Text>

            <input
              type="file"
              accept=".pdf,image/png,image/jpeg"
              onChange={onFileChange}
            />

            {file && <Text color="gray">Archivo: {file.name}</Text>}
            {error && <Text color="red">{error}</Text>}

            <Flex justify="end">
              <Button disabled={!file || isPending} onClick={handleEnviar}>
                {isPending ? <Spinner /> : 'Enviar comprobante'}
              </Button>
            </Flex>

            <Text color="gray" size="2">
              Tamaño máximo: {MAX_MB} MB. Formatos permitidos: PDF, JPG, PNG.
            </Text>
          </Flex>
        )}
      </Flex>
    </Flex>
  )
}
