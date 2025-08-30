import { SumexusSettingsInterfaceProps } from '@/types/settings'


const Copyright: React.FC<SumexusSettingsInterfaceProps> = ({ props }) => {
  return (
    <div className='text-center py-10 border-t text-sm'>
      Copyright &copy; {props.name} LLC 2024. All rights reserved.
    </div>
  )
}

export default Copyright
