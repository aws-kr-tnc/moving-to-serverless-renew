import { shallowMount } from '@vue/test-utils';
import LayoutBody from '@/components/layout/LayoutBody.vue';

describe('LayoutBody', () => {
  const wrapper = shallowMount(LayoutBody);

  it('renders router', () => {
    expect(wrapper.find('router-view-stub').exists()).toMatchSnapshot();
  });

  it('renders v-content', () => {
    expect(wrapper.find('v-content-stub').exists()).toBe(true);
  });
});
