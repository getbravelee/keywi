import MainButton from '@/components/MainButton'
import { Text } from '@/styles/typography'
import { colors } from '@/styles/colors'
import tw from 'twin.macro'
import { CheckCircleSolid } from 'iconoir-react'
import { useDealAcceptStore } from '@/stores/chatStore'

const Container = tw.div`
  flex flex-col items-center justify-center h-screen px-4
`

export default function AcceptCompleteScreen({
  onConfirm,
}: {
  onConfirm: () => void
}) {
  const receipt = useDealAcceptStore((state) => state.receipt)

  return (
    <Container>
      <div className="flex flex-col items-center py-56 text-center gap-4">
        <CheckCircleSolid height={`5rem`} width={`5rem`} color={colors.kiwi} />
        <Text variant="title2" weight="bold" color="black">
          {receipt.totalAmount.toLocaleString()}원을 결제하고
          <br />
          안심결제 진행중이에요
        </Text>
        <Text variant="caption1" weight="bold" color="gray">
          거래가 완료될 때까지 조립자에게
          <br />
          돈이 전달되지 않으니 걱정 마세요!
        </Text>
      </div>

      <div className="w-full mt-auto mb-12">
        <MainButton text="확인" onClick={onConfirm}></MainButton>
      </div>
    </Container>
  )
}
